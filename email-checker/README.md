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

## Limits
2 checks at once, 1 second between starts, 400 checks per India day, 60 s per check, results kept 14 days (valid, invalid,
accept_all). If the Mac is off or asleep the relay answers "unknown, checker offline" and the round falls back to Hunter.

## Not for other users
A home address must not serve other users. Later, move this to a rented server that allows port 25: same code, run `server.mjs`
there behind a real tunnel or domain.
