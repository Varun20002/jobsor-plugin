// Relay: a stable public URL in front of the Mac's changing tunnel URL.
const OFFLINE = { status: 'unknown', reason: 'checker offline (laptop off or asleep)', warning: 'Email checker offline (Mac off or asleep). Hunter is used instead.' };

function same(a, b) {
  if (a.length !== b.length) return false;
  let d = 0;
  for (let i = 0; i < a.length; i++) d |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return d === 0;
}

export async function handleRequest(request, env, fetchFn = fetch) {
  const url = new URL(request.url);
  const path = url.pathname;
  if (path === '/' && request.method === 'GET') return new Response('JOBSOR email checker relay', { headers: { 'content-type': 'text/plain' } });

  if (path === '/register' && request.method === 'POST') {
    const given = request.headers.get('x-checker-secret') || '';
    if (!env.CHECKER_SECRET || !same(given, env.CHECKER_SECRET)) return new Response('unauthorized', { status: 401 });
    let body;
    try { body = await request.json(); } catch { return new Response('bad body', { status: 400 }); }
    if (!body || typeof body.url !== 'string' || !/^https:\/\/[a-z0-9.-]+$/i.test(body.url)) return new Response('bad url', { status: 400 });
    await env.TUNNEL.put('url', body.url);
    return new Response('ok');
  }

  const m = path.match(/^\/mcp\/([^/]+)$/);
  if (!m || !env.CHECKER_SECRET || !same(m[1], env.CHECKER_SECRET)) return new Response('not found', { status: 404 });

  const bodyText = request.method === 'GET' || request.method === 'HEAD' ? undefined : await request.text();
  let rpc = null;
  try { rpc = bodyText ? JSON.parse(bodyText) : null; } catch {}
  const offline = () => {
    if (rpc && rpc.method === 'tools/call') {
      return Response.json({ jsonrpc: '2.0', id: rpc.id, result: { content: [{ type: 'text', text: JSON.stringify(OFFLINE) }] } });
    }
    return new Response('checker offline', { status: 502 });
  };

  const target = await env.TUNNEL.get('url');
  if (!target) return offline();
  const headers = new Headers();
  for (const h of ['content-type', 'accept', 'mcp-session-id', 'mcp-protocol-version']) {
    const v = request.headers.get(h);
    if (v) headers.set(h, v);
  }
  headers.set('x-checker-secret', env.CHECKER_SECRET);
  try {
    const res = await fetchFn(`${target}/mcp`, { method: request.method, headers, body: bodyText, signal: AbortSignal.timeout(75000) });
    return new Response(res.body, { status: res.status, headers: res.headers });
  } catch {
    return offline();
  }
}

export default { fetch: (request, env) => handleRequest(request, env) };
