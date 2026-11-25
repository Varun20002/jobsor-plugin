// JOBSOR email checker: a tiny MCP server (one tool, verify_email) that runs Reacher.
// Runs on the owner's Mac. Node built-ins only.
import http from 'node:http';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import crypto from 'node:crypto';
import { execFile } from 'node:child_process';

const HOME = process.env.HOME || os.homedir();
const DIR = path.join(HOME, '.jobsor-checker');
const CACHE_FILE = path.join(DIR, 'cache.json');
const DAY_FILE = path.join(DIR, 'day.json');
const SECRET = process.env.CHECKER_SECRET || '';
const BIN = process.env.REACHER_BIN || '';
const PORT = Number(process.env.PORT || 8099);
const DAILY = Number(process.env.CHECKER_DAILY || 400);
const TIMEOUT_MS = Number(process.env.CHECKER_TIMEOUT_MS || 60000);
const MAX_PARALLEL = 2;
const GAP_MS = Number(process.env.CHECKER_GAP_MS || 1000);
const CACHE_DAYS = 14;

fs.mkdirSync(DIR, { recursive: true });

function readJson(file, fallback) {
  try { return JSON.parse(fs.readFileSync(file, 'utf8')); } catch { return fallback; }
}
function writeJson(file, data) {
  try { fs.writeFileSync(file, JSON.stringify(data)); } catch {}
}

// India day = UTC + 5:30
function indiaDay() {
  return new Date(Date.now() + 5.5 * 3600 * 1000).toISOString().slice(0, 10);
}

function same(a, b) {
  const x = Buffer.from(String(a)); const y = Buffer.from(String(b));
  return x.length === y.length && crypto.timingSafeEqual(x, y);
}

function mask(email) {
  const [u, d] = email.split('@');
  return `${u[0] || ''}***@${d}`;
}

function mailHost(records) {
  if (!records || !records.length) return 'none';
  const s = records.join(' ').toLowerCase();
  if (/google|googlemail/.test(s)) return 'google';
  if (/outlook|protection\.outlook|microsoft/.test(s)) return 'microsoft';
  if (/zoho/.test(s)) return 'zoho';
  if (/mimecast/.test(s)) return 'mimecast';
  return 'other';
}

// Queue: at most 2 at once, at least GAP_MS between starts.
let running = 0;
let lastStart = 0;
const waiting = [];
function schedule(task) {
  return new Promise((resolve) => { waiting.push({ task, resolve }); pump(); });
}
function pump() {
  if (running >= MAX_PARALLEL || !waiting.length) return;
  const wait = lastStart + GAP_MS - Date.now();
  if (wait > 0) { setTimeout(pump, wait); return; }
  const { task, resolve } = waiting.shift();
  running++;
  lastStart = Date.now();
  task().then(resolve, () => resolve(null)).finally(() => { running--; pump(); });
  pump();
}

function runReacher(email) {
  return new Promise((resolve) => {
    execFile(BIN, [email], { timeout: TIMEOUT_MS, maxBuffer: 4 * 1024 * 1024 }, (err, stdout) => {
      if (err && err.killed) return resolve({ error: 'timeout' });
      try { resolve({ json: JSON.parse(stdout) }); } catch { resolve({ error: 'unreadable' }); }
    });
  });
}

function mapResult(email, j) {
  const host = mailHost(j.mx && j.mx.records);
  const catchAll = !!(j.smtp && j.smtp.is_catch_all);
  let status = 'unknown'; let reason = 'could not tell';
  if (j.is_reachable === 'safe') { status = 'valid'; reason = 'mail server accepted the address'; }
  else if (j.is_reachable === 'invalid') { status = 'invalid'; reason = 'mail server refused the address'; }
  else if (j.is_reachable === 'risky' && catchAll) { status = 'accept_all'; reason = 'server accepts every address'; }
  else if (j.is_reachable === 'risky') { reason = 'risky, not a catch-all'; }
  return { email, status, accept_all: status === 'accept_all', mail_host: host, reason, checked_by: 'reacher', cached: false };
}

async function verify(email) {
  const key = email.toLowerCase();
  const cache = readJson(CACHE_FILE, {});
  const hit = cache[key];
  if (hit && Date.now() - hit.at < CACHE_DAYS * 86400000) {
    return { ...hit.result, cached: true };
  }
  // daily limit
  const day = readJson(DAY_FILE, {});
  const today = indiaDay();
  let count = day.day === today ? day.count : 0;
  if (count >= DAILY) {
    return { email, status: 'unknown', accept_all: false, mail_host: 'none', reason: 'daily limit', checked_by: 'reacher', cached: false };
  }
  writeJson(DAY_FILE, { day: today, count: count + 1 });
  const out = await schedule(() => runReacher(key));
  let result;
  if (!out || out.error) {
    result = { email, status: 'unknown', accept_all: false, mail_host: 'none', reason: out && out.error === 'timeout' ? 'check timed out' : 'check failed', checked_by: 'reacher', cached: false };
  } else {
    result = mapResult(email, out.json);
  }
  console.log(`${new Date().toISOString()} ${mask(email)} ${result.status}`);
  if (result.status !== 'unknown') {
    const c = readJson(CACHE_FILE, {});
    c[key] = { result, at: Date.now() };
    writeJson(CACHE_FILE, c);
  }
  return result;
}

const TOOL = {
  name: 'verify_email',
  description: "Check whether a work email address exists, by asking the company's mail server (no email is sent). Returns status valid, invalid, accept_all or unknown.",
  inputSchema: { type: 'object', properties: { email: { type: 'string', description: 'The address to check' } }, required: ['email'] },
};

async function handle(msg) {
  const { id, method, params } = msg;
  const ok = (result) => ({ jsonrpc: '2.0', id, result });
  const bad = (code, message) => ({ jsonrpc: '2.0', id, error: { code, message } });
  if (method === 'initialize') {
    return ok({
      protocolVersion: (params && params.protocolVersion) || '2025-06-18',
      capabilities: { tools: {} },
      serverInfo: { name: 'jobsor-email-checker', version: '0.1.0' },
      instructions: 'Use verify_email to check a work address before sending; it never sends mail.',
    });
  }
  if (method === 'ping') return ok({});
  if (method === 'tools/list') return ok({ tools: [TOOL] });
  if (method === 'tools/call') {
    const name = params && params.name;
    if (name !== 'verify_email') return bad(-32602, 'unknown tool');
    const email = String((params.arguments && params.arguments.email) || '').trim();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email) || email.length > 200) {
      return ok({ isError: true, content: [{ type: 'text', text: 'Not a valid address shape.' }] });
    }
    const result = await verify(email);
    return ok({ content: [{ type: 'text', text: JSON.stringify(result) }] });
  }
  return bad(-32601, 'method not found');
}

const server = http.createServer((req, res) => {
  const send = (code, body, type = 'application/json') => {
    res.writeHead(code, { 'content-type': type });
    res.end(body === undefined ? '' : (typeof body === 'string' ? body : JSON.stringify(body)));
  };
  const url = (req.url || '').split('?')[0];
  if (req.method === 'GET' && url === '/health') return send(200, { ok: true });
  if (!SECRET || !same(req.headers['x-checker-secret'] || '', SECRET)) return send(401, { error: 'unauthorized' });
  if (url !== '/mcp') return send(404, { error: 'not found' });
  if (req.method === 'GET') return send(405, { error: 'method not allowed' });
  if (req.method !== 'POST') return send(405, { error: 'method not allowed' });
  let body = '';
  req.on('data', (c) => { body += c; if (body.length > 100000) req.destroy(); });
  req.on('end', async () => {
    let msg;
    try { msg = JSON.parse(body); } catch { return send(400, { jsonrpc: '2.0', id: null, error: { code: -32700, message: 'parse error' } }); }
    if (Array.isArray(msg)) return send(200, { jsonrpc: '2.0', id: null, error: { code: -32600, message: 'batches not supported' } });
    if (msg.method && msg.method.startsWith('notifications/')) { res.writeHead(202); return res.end(); }
    if (msg.id === undefined) { res.writeHead(202); return res.end(); }
    try { send(200, await handle(msg)); } catch { send(200, { jsonrpc: '2.0', id: msg.id, error: { code: -32603, message: 'internal error' } }); }
  });
});

server.listen(PORT, '127.0.0.1', () => console.log(`email checker on 127.0.0.1:${PORT}`));
