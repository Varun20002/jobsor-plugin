# JOBSOR

Job search for India that gets you to a person, not a portal. JOBSOR finds fresh jobs, decides whether the company is a startup or an MNC,
finds the right person to write to (hiring manager, founder, recruiter or referrer) with proof they work there now, finds their email,
writes a short researched message from facts you confirmed, sends it from your own Gmail or leaves it as a draft, and follows up until
someone at the company replies.

## Use it

1. Turn on **Claude's own Gmail connector** (claude.ai: Settings, then Connectors, then Gmail, then Connect). Then add the plugin, open its
   **Connectors** tab and connect **Exa** and **Firecrawl**. Optional: Apify (LinkedIn jobs), Hunter, Indeed, and
   Vibe Prospecting (Claude's own Connectors; a backup when Hunter runs out).
   Gmail is not inside the plugin on purpose: Google's sign-in refuses connectors that register themselves, so only Claude's own Gmail
   connector can sign in.
2. Type `/jobsor:start`. JOBSOR checks your connectors and tells you what to do next.
3. Setup reads your resume, asks a few questions, and makes two files in your account: your JOBSOR profile and your tracker. It also sets
   up "JOBSOR round", an hourly scheduled task (quiet from 12 midnight to 9 AM India time).
4. Each round: replies and bounces first, then due follow-ups, then new jobs from your alert emails (the LinkedIn post search three times a day), the right people, and messages, sent
   from your Gmail (up to your daily limit; a guessed address is checked first, then sent). Each job's email carries its own one-page resume, tailored from your own resume lines.
   Set it up on claude.ai and the hourly round runs in the cloud, with your laptop closed. You can also run any step yourself: `/jobsor:find-jobs`, `/jobsor:find-people`,
   `/jobsor:write`, `/jobsor:send`, `/jobsor:round`.

**After an update:** type `/jobsor:update` once. It runs only what is new (for example a new alert check) and never redoes setup.

In Cowork and Claude Code, two helpers (people-finder, researcher) let a round work on several jobs at once, and a guard refuses any
Gmail send outside 9 AM to 12 midnight India time or above 100 in a day.

## Rules it always keeps

- It writes only what you confirmed about yourself. Nothing is invented.
- It never contacts anyone on LinkedIn for you and never logs in to LinkedIn.
- It sends by itself by default, within a daily limit (100 by default and at most, 9 AM to midnight India time). Say "drafts" to turn that off. Replies are always drafts.
- It stops everything to a company (messages, drafts, follow-ups) the moment anyone at that company replies.

## Your data

Everything stays in your own Claude account and your own Gmail. JOBSOR has no server in this version: it sends nothing to JOBSOR.
Gmail is used to read job-alert emails and replies, and to save drafts or send your messages. Exa and Firecrawl receive search queries
(a company, a role, a person's name) and the addresses of public pages to read; through Firecrawl, LinkedIn's public post search is
queried by a third party (HarvestAPI) with no LinkedIn login. Apify, if connected, runs a LinkedIn jobs search on your own Apify account. Mail text is never copied into your tracker; only links,
titles, companies, names and dates are kept.
