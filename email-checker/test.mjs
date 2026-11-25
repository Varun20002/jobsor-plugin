// node --test email-checker/   (no network)
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { handleRequest } from './relay/worker.js';

const here = path.dirname(new URL(import.meta.url).pathname);
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'checker-'));
const fake = path.join(tmp, 'fake.sh');
const runlog = path.join(tmp, 'runs.txt');
fs.writeFileSync(fake, `#!/bin/bash
echo "$1" >> ${runlog}
case "$1" in
  safe@*) echo '{"is_reachable":"safe","mx":{"records":["aspmx.l.google.com."]},"smtp":{"is_catch_all":false}}';;
  bad@*) echo '{"is_reachable":"invalid","mx":{"records":["x.zoho.com."]},"smtp":{"is_catch_all":false}}';;
  catch@*) echo '{"is_reachable":"risky","mx":{"records":["a.mimecast.com."]},"smtp":{"is_catch_all":true}}';;
  slow@*) sleep 5;;
  *) echo '{"is_reachable":"unknown","mx":{"records":[]},"smtp":{"is_catch_all":false}}';;
esac
`, { mode: 0o755 });

const PORT = 18099;
let proc;
const H = { 'content-type': 'application/json', 'x-checker-secret': 's3cret' };
const rpc = (method, params, id = 1, headers = H) =>
  fetch(`http://127.0.0.1:${PORT}/mcp`, { method: 'POST', headers, body: JSON.stringify({ jsonrpc: '2.0', id, method, params }) });
const call = async (email) => {
  const r = await (await rpc('tools/call', { name: 'verify_email', arguments: { email } })).json();
  return r.result;
};
const runs = () => (fs.existsSync(runlog) ? fs.readFileSync(runlog, 'utf8').trim().split('\n').filter(Boolean).length : 0);

test.before(async () => {
  proc = spawn('node', [path.join(here, 'server.mjs')], {
    env: { ...process.env, HOME: tmp, PORT: String(PORT), CHECKER_SECRET: 's3cret', REACHER_BIN: fake, CHECKER_DAILY: '6', CHECKER_TIMEOUT_MS: '1500', CHECKER_GAP_MS: '10' },
    stdio: 'ignore',
  });
  for (let i = 0; i < 50; i++) {
    try { if ((await fetch(`http://127.0.0.1:${PORT}/health`)).ok) return; } catch {}
    await new Promise((r) => setTimeout(r, 100));
  }
});
test.after(() => proc.kill());

test('initialize, list, auth', async () => {
  const init = await (await rpc('initialize', { protocolVersion: '2025-03-26' })).json();
  assert.equal(init.result.protocolVersion, '2025-03-26');
  assert.equal(init.result.serverInfo.name, 'jobsor-email-checker');
  const list = await (await rpc('tools/list')).json();
  assert.equal(list.result.tools[0].name, 'verify_email');
  const unk = await (await rpc('nope')).json();
  assert.equal(unk.error.code, -32601);
  assert.equal((await rpc('tools/list', {}, 1, { ...H, 'x-checker-secret': 'wrong' })).status, 401);
  assert.equal((await fetch(`http://127.0.0.1:${PORT}/mcp`, { headers: H })).status, 405);
});

test('statuses, cache, bad email', async () => {
  const parse = (r) => JSON.parse(r.content[0].text);
  assert.equal(parse(await call('safe@a.com')).status, 'valid');
  assert.equal(parse(await call('bad@a.com')).status, 'invalid');
  const c = parse(await call('catch@a.com'));
  assert.equal(c.status, 'accept_all'); assert.equal(c.accept_all, true); assert.equal(c.mail_host, 'mimecast');
  const before = runs();
  const again = parse(await call('safe@a.com'));
  assert.equal(again.cached, true);
  assert.equal(runs(), before);
  assert.equal(parse(await call('who@a.com')).status, 'unknown');
  const bad = await call('not-an-email');
  assert.equal(bad.isError, true);
});

test('timeout gives unknown, then daily limit', async () => {
  const parse = (r) => JSON.parse(r.content[0].text);
  const slow = parse(await call('slow@a.com'));
  assert.equal(slow.status, 'unknown');
  // 5 real checks have started so far (safe, bad, catch, who, slow); limit is 6
  assert.notEqual(parse(await call('who2@a.com')).reason, 'daily limit');
  const over = parse(await call('who3@a.com'));
  assert.equal(over.status, 'unknown'); assert.equal(over.reason, 'daily limit');
});

// relay
const kv = () => { const m = new Map(); return { get: async (k) => m.get(k) ?? null, put: async (k, v) => { m.set(k, v); } }; };
const env = () => ({ CHECKER_SECRET: 'abc', TUNNEL: kv() });
const post = (p, body, headers = {}) => new Request(`https://r.dev${p}`, { method: 'POST', headers: { 'content-type': 'application/json', ...headers }, body: JSON.stringify(body) });

test('relay: register, 404, offline, proxy', async () => {
  const e = env();
  assert.equal((await handleRequest(post('/register', { url: 'https://x.trycloudflare.com' }, { 'x-checker-secret': 'no' }), e)).status, 401);
  const call = { jsonrpc: '2.0', id: 7, method: 'tools/call', params: { name: 'verify_email', arguments: { email: 'a@b.co' } } };
  assert.equal((await handleRequest(post('/mcp/wrong', call), e)).status, 404);
  // nothing registered: offline result
  const off = await (await handleRequest(post('/mcp/abc', call), e)).json();
  assert.equal(off.id, 7);
  assert.equal(JSON.parse(off.result.content[0].text).status, 'unknown');
  assert.equal((await handleRequest(post('/mcp/abc', { jsonrpc: '2.0', id: 1, method: 'tools/list' }), e)).status, 502);
  assert.equal((await handleRequest(post('/register', { url: 'https://x.trycloudflare.com' }, { 'x-checker-secret': 'abc' }), e)).status, 200);
  // fetch fails: still offline result
  const failing = async () => { throw new Error('down'); };
  const off2 = await (await handleRequest(post('/mcp/abc', call), e, failing)).json();
  assert.equal(JSON.parse(off2.result.content[0].text).status, 'unknown');
  // proxy works and adds secret header
  let seen;
  const fakeFetch = async (u, init) => { seen = { u, h: init.headers }; return new Response('{"ok":1}', { status: 200 }); };
  const ok = await handleRequest(post('/mcp/abc', call), e, fakeFetch);
  assert.equal(await ok.text(), '{"ok":1}');
  assert.equal(seen.u, 'https://x.trycloudflare.com/mcp');
  assert.equal(seen.h.get('x-checker-secret'), 'abc');
});
