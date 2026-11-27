# JOBSOR email checker (owner only)

A tiny connector with one tool, `verify_email`. It asks a company's mail server whether an address exists (Reacher, no email is
sent) and answers valid, invalid, accept_all or unknown. The JOBSOR plugin calls it before Hunter. It runs on the owner's Mac,
because a home internet line allows outbound port 25. Not published; only the owner adds it.

Parts: `server.mjs` (the connector, on the Mac), `relay/` (a free Cloudflare Worker `jobsor-email-checker` with a stable address),
`start.sh` (server + quick tunnel + registers the tunnel with the relay), `install.sh` / `uninstall.sh` (LaunchAgent).

## Install
1. Deploy the relay once: `cd relay`, create the KV namespace (`npx wrangler kv namespace create TUNNEL`), put its id in
   `wrangler.jsonc`, `npx wrangler deploy`, then set the secret `CHECKER_SECRET` with `npx wrangler secret put CHECKER_SECRET`
   (same value as `~/.jobsor-checker/secret`).
2. Save the relay address in `~/.jobsor-checker/relay-url.txt`.
3. `bash install.sh /path/to/check_if_email_exists`

## Add to claude.ai
Settings > Connectors > Add custom connector > paste the address from `~/.jobsor-checker/connector-url.txt` (no OAuth). The
address contains the secret: do not share it or paste it in chat.

## Uninstall
`bash uninstall.sh` (keeps the cache and secret in `~/.jobsor-checker`).

## How it connects (version 0.2.0)
Claude (cloud) -> relay `https://jobsor-email-checker.<account>.workers.dev/mcp/<secret>` -> the Mac's quick tunnel (`cloudflared`)
-> `server.mjs` on 127.0.0.1:8099 -> Reacher -> the company's mail server on port 25. The quick tunnel's own address changes on every
restart; `start.sh` re-registers it with the relay (POST /register), so the connector address never changes. It changes only if the
secret changes. The LaunchAgent starts at login (not before), and `caffeinate` stops idle sleep while it runs.

## Tools and answers
- `verify_email {email}` -> JSON text {email, status valid|invalid|accept_all|unknown, accept_all, mail_host, reason, checked_by,
  cached, warning?}. The plugin's send hook recognises it because the tool name contains "verif".
- `checker_status` -> {day, checks_today, limit, streak, last_ok_at, warning?}.
- Warnings: "daily limit of 400 reached"; "may be blocked" after 5 checks in a row that reached no mail server (state in
  `~/.jobsor-checker/health.json`); the relay's "offline (Mac off or asleep)" when the Mac does not answer.

## Limits
2 checks at once, 1 second between starts, 400 checks per India day, 60 s per check, results kept 14 days (valid, invalid,
accept_all). If the Mac is off or asleep the relay answers "unknown, checker offline" and the round falls back to Hunter.

## Files on the Mac (`~/.jobsor-checker/`, not in git)
`secret`, `relay-url.txt`, `connector-url.txt` (contains the secret), `cache.json`, `day.json`, `health.json`, `log/`, `bin/` (Reacher).
Check it: `launchctl list | grep jobsor` and `curl -s http://127.0.0.1:8099/health`. Restart: `launchctl kickstart -k gui/$(id -u)/com.jobsor.emailchecker`.
Tests: `node --test email-checker/test.mjs` (fake Reacher, no network). Relay deploy: `cd email-checker/relay && npx wrangler deploy`.

## Not for other users
A home address must not serve many users. Sharing the connector address with 5 to 10 friends for a test is acceptable (they share
the 400 checks; one user needs about 10 to 30 a day). Later, move this to a rented server that allows port 25 (about EUR 4-5 a
month), with a key per user: same code, run `server.mjs` there behind a real tunnel or domain.
