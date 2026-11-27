# JOBSOR plugin: instructions for any Claude working in this repo

Claude reads this file when a session starts in this folder. Read it fully, then `docs/HANDOVER.md` (where things stand), then
`docs/DECISIONS.md` (what was decided and why) before changing anything.

## 1. What this repo is
- **JOBSOR** is a Claude plugin for job seekers in India. Each hourly "round" (a scheduled task, usually in Claude's cloud with the
  laptop closed): checks replies and bounces, sends due follow-ups, finds fresh jobs, finds the right people at each company with
  proof they work there now, finds and checks their emails, writes short messages from the user's confirmed facts only, sends them from
  the user's Gmail (or leaves drafts), and reports. All state lives in the user's own tracker (a claude.ai spreadsheet artifact) and
  profile; JOBSOR has no server.
- Repo: github.com/Varun20002/jobsor-plugin (this folder, `/Users/varuna.r/jobsor-plugin`). Branch `main`.
  - `plugins/jobsor/`: the plugin itself (skills, agents, hooks, scripts). See section 4.
  - `email-checker/`: the owner's private email checker connector (runs on the owner's Mac). See `email-checker/README.md`.
  - `.claude-plugin/marketplace.json`: the marketplace that lists the plugin.
  - `docs/`: handover, decisions, research notes.
- The **main project** `/Users/varuna.r/jobsor` (github.com/Varun20002/jobsor) is the older web app. It is **frozen**: never commit or
  push to it (owner's order, 21 Nov 2026). Its `CLAUDE.md` and `docs/` are useful background only. Two things there are still used by
  the plugin release (section 5): `scripts/build-plugin.mjs` and `data/verified-boards.json`. Their output there stays uncommitted.

## 2. The owner and how to work with him
- **Owner: Varun** (GitHub `Varun20002`). **Not a developer.** Plain, short words. Exactly what to click or paste. One terminal command
  per code block. If he says "I don't understand", re-explain simply, one step at a time.
- He already has a job; JOBSOR is a product he wants to monetize and use to help people (not his own job hunt). Build for many users on
  free plans, each bringing their own keys. Examples in skills must be general (any field), never about one real person.
- **Standing rules (his words):**
  - "Please don't do edits when I don't say it." Questions get answers only. Change exactly what he asked, nothing extra. If something
    else seems wise, say it in one line and ask.
  - "Our scope here is only JOBSOR plugin." Commit and push only this repo.
  - "Use Opus as advisor and Sonnet as executor." For a real change: Opus reads the code and writes a precise spec (in the session
    scratchpad), a Sonnet subagent makes the change and runs the tests, Opus reviews the diff (it has caught real bugs), then releases.
- **Ask first:** anything that costs money; tests on real accounts (Hunter, Apollo, Gmail, LinkedIn); anything that messages someone
  other than the owner; network runs longer than about 2 minutes.
- **Secrets never go in chat or in files** (including the email checker's connector address, which contains its secret).
- Report honestly: what was verified, what was NOT.

## 3. Hard product rules (the skills enforce them; keep them)
- Messages and resumes use only facts the user confirmed. Nothing invented.
- Never contacts anyone on LinkedIn and never logs in to LinkedIn.
- Sends by default within the user's daily cap (default 50, never above 50), 9 AM to 12 midnight India time. Replies are always drafts.
- Email labels: `published`, `checked`, `checked (accept-all)`, `guessed (not checked)`. An unchecked guess is never sent (0.2.45).
- Stops following up on a job when anyone at that company replies.

## 4. Plugin layout (`plugins/jobsor/`)
- `.claude-plugin/plugin.json`: name and **version** (bump on every release).
- `skills/`: `start`, `setup`, `update`, `round`, `find-jobs`, `route`, `find-people`, `find-email`, `write`, `resume`, `send`. Each has
  a `SKILL.md`, some have `references/` and `scripts/`.
  - `skills/round/scripts/jobsor.py` (+ `test_jobsor.py`): rules kept by code: `plan` (which sources are due this window), `score`
    (Match: Work 45 + Must 40 + Level 15/12/8, stretch cap 60), `people` (target counts per route, keeps a log), `indeed-hook`,
    `stop-hook` (a round cannot end with due sources unrun or a contacted job's people count short).
  - `skills/send/scripts/check_message.py` (+ `test_check_message.py`): message checks; in hook mode it also refuses a new email to an
    address that was not checked in this run.
  - `skills/update/references/changes.md`: one entry per version; `/jobsor:update` runs only the "Step" entries a user has not run.
  - `skills/round/references/shared-rules.md`, `debug-log.md` (Debug steps / Debug emails / Debug jobs tabs, only when the profile
    says "Debug log: on").
  - `skills/setup/references/tracker-columns.md` and `profile-template.md`: the tracker tabs and the profile.
- `agents/`: `people-finder`, `researcher` (helpers for parallel work in a round).
- `hooks/hooks.json`: PreToolUse on Gmail sends -> `scripts/send-guard.sh` (hours, 50 a day, then `check_message.py --hook`);
  PreToolUse on Indeed `search_jobs` -> `jobsor.py indeed-hook`; Stop -> `jobsor.py stop-hook`. Hooks also run in Claude's cloud
  (tested 22 and 24 Nov 2026). Files written to disk do not survive between cloud runs.
- `.mcp.json`: connectors shipped with the plugin: Exa, Firecrawl, Apify, Indeed. Gmail is Claude's own connector (Google refuses
  self-registered connectors). Hunter and Vibe Prospecting are optional Claude connectors the user adds.
- `evals/` is excluded from the zip.

## 5. Tests and release (every change)
1. Tests, from `plugins/jobsor/`:
   - `python3 -I skills/round/scripts/test_jobsor.py` (33 at 0.2.48)
   - `python3 -I skills/send/scripts/test_check_message.py` (28 at 0.2.48)
   - if `email-checker/` changed: `node --test email-checker/test.mjs` from the repo root (6 at checker 0.2.0)
2. Bump `plugins/jobsor/.claude-plugin/plugin.json` and add an entry to `skills/update/references/changes.md` ("No step to run." unless
   the user must answer something new).
3. Copy into the main folder and build the zip (the build checks that no skill description has angle brackets, which claude.ai refuses):
   - `rsync -a --delete --exclude evals --exclude '.DS_Store' /Users/varuna.r/jobsor-plugin/plugins/jobsor/ /Users/varuna.r/jobsor/plugin/jobsor/`
   - `cd /Users/varuna.r/jobsor && node scripts/build-plugin.mjs` -> `/Users/varuna.r/jobsor/plugin/jobsor.zip` (do not commit there)
4. Commit and push **this repo only**, message "JOBSOR plugin 0.2.NN: <what changed>".
5. Update the owner's local install (Claude desktop's bundled CLI):
   `C=$(ls ~/Library/Application\ Support/Claude/claude-code/*/*/claude.app/Contents/MacOS/claude | tail -1); "$C" plugin marketplace update jobsor; "$C" plugin update jobsor@jobsor`
6. Send the zip to the owner. **The cloud only gets the new version after he uploads the zip on claude.ai** (Customize > Plugins).
   `/jobsor:update` is needed only when changes.md has a "Step".

## 6. Where to look when something goes wrong
- The owner's tracker (claude.ai artifact `DKovRctDYq6vwWnEHAK4wv`, engine workbook): tabs Jobs, People, Messages, Seen, Log, and the
  debug tabs. Read it with the docs connector (`readCells`), only the tabs needed. Never paste people's details into other services.
- A chat that started before an update keeps the old plugin copy and may show old stop-hook messages ("jobsor@inline"): ignore them or
  start a new chat.

## 7. Memory that does not travel between Claude accounts
Connectors (Gmail, Exa, Firecrawl, Apify, Hunter, the email checker), the Chrome extension pairing, permission approvals and Claude's
own memory files belong to an account. Logins that live on the owner's Mac (git push, Cloudflare `wrangler`, Google Cloud, the VM's
SSH key) work from any account. Everything a new account needs to know is in this file and `docs/`.
