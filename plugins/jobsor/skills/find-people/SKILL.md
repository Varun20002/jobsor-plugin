---
name: find-people
description: Find the right people to contact for a job in the JOBSOR tracker (hiring manager, founder, recruiter, referrer), each with proof they work at the company now. Use when the user asks "who is the hiring manager", "find people for this job", "who should I write to at this company", pastes a hiring-team screenshot, or when the JOBSOR round reaches a job with no people yet.
---

# Find people, with proof

Read the JOBSOR profile and the job's row first. The route skill has set Size (Startup, MNC, Agency) and who to look for; if it has not,
run route first. Then search in the order below and **stop as soon as the right person is found with proof**: a confirmed hiring manager
at a startup (or, without one, the peers to ask); the recruiter and up to 2 referrers at an MNC; the posting recruiter for an agency.

**Before anyone is written to the People tab, apply `references/proof-rules.md`.** A person goes in only with a proof they work at this
company now and no contradiction. Unsure means left out. Never relax the proof to fill the list. Write the proof in plain words in the
Proof column.

## Order of search

1. **The hiring post itself.** If the job came from a LinkedIn or X post, the round must check the poster before anyone else, every
   time, and write the result. Also check anyone the post names ("reach out to Priya", "DM me", "my team"). Their own hiring post for
   this job is a proof.
   - Poster works at the company now (proof: their headline names the company, or the company's team page lists them): add them first.
     Contact as Recruiter if their title or post says recruiter, HR, talent or people team; otherwise Hiring manager.
   - Poster is a job-sharing page, a recruitment agency or someone not at the company: do not add them. Write in the job's Notes
     "Poster <name> is not at <company> (<why>)" and go on to step 2.
   Never skip this check, even when a founder or leader is easy to find.
2. **Reverse search from the job link** (the job came from a job link or an apply link and nobody is named). Search Exa and Firecrawl for
   LinkedIn and X posts that share **this same link**, three ways, because posts often hold a short link (lnkd.in, bit.ly) instead of the
   long one:
   - the link itself and its short forms: the LinkedIn job id (`jobs/view/<id>`, search the id), the hiring-system path
     (`jobs.lever.co/<company>/<id>`, `job-boards.greenhouse.io/<company>/jobs/<id>`, `jobs.ashbyhq.com/<company>/<id>`), a Google Form id;
   - the exact job title with the company name and a hiring word: `"<title>" "<company>" (hiring OR "we're looking for" OR apply)`;
   - for a LinkedIn job link, Exa's copy of the job page, which sometimes names the poster or the hiring team.
   Also run LinkedIn's own post search through Firecrawl (`firecrawl_scrape` with `alexandria`
   `{"provider": "harvestapi", "capability": "linkedin/search-posts", "options": {"search": "<title> <company>", "postedLimit": "month",
   "sortBy": "date"}}`, about 2 credits), which finds posts Exa does not have.
   A post counts only if it names this company and this role (or links this job) and is from the last 30 days; then the poster has the
   "own hiring post" proof. Job-sharing accounts and recruitment agencies are not the hiring manager: keep one as a recruiter only if they
   work at the company.
3. **The usual sources.**
   - A "Meet the hiring team" screenshot the user pasted: trusted as is for this job (LinkedIn's own box), even an agency recruiter.
   - Headline searches with Exa: `"<role or function> at <company>"`, `"head of <function>" "<company>"`, `"founder" "<company>"`
     (startups), `"talent acquisition" "<company>" India` (MNC recruiter). Read results as people only when the line is theirs.
   - The company's own team or about page (`/team`, `/about`, `/company`), read with Firecrawl.
   - Hunter's people at the company's domain, if Hunter is connected (a Hunter record alone is not proof; it needs a public line that
     agrees).
   - **Last, the wide backup: Vibe Prospecting**, only if it is connected (optional) and only when Exa, Firecrawl and Hunter found
     nobody fitting, or Hunter is out of credits: `match-business` for the company, then `fetch-entities` for prospects at it by title
     (hiring manager's function, founder, recruiter or talent acquisition, India). At most 1 search a job, to save its small free credits.
     A Vibe record alone is not proof: it needs a public line that agrees (post, headline, team page). If it says no credits, skip it
     for the rest of the day.
4. **Startup with no confirmed hiring manager: ask peers.** Never guess the hiring manager from a title. If steps 1 to 3 did not find a
   person confirmed as hiring for this role (see "Who counts as the hiring manager"), do not pitch anyone: ask 2 peers who the hiring
   manager is. A founder, a "founding team" member or a head of the function is **not** assumed to be the hiring manager; they are
   pitched only when confirmed. If no peer in the same team can be found (a very small company), ask a founder the same question
   instead of pitching them.
   **Ask a peer (startups only).** Find 2 people in the same team (1 if only one exists) (same function, with proof they work there
   now) and add them with Contact as "Peer (to ask)". The write skill gives them the peer ask: "Do you know who the hiring manager for this
   role is?" It is never a pitch and never asks for a referral. When a peer replies with a name, the round adds that person with the proof
   "Named by <peer> in a reply" and drafts the pitch to them. At an MNC the peer step is not used.
5. **Then pitch.** Only once the right person is found does the write skill write to them.

## Who counts as the hiring manager
Only a person **confirmed** as hiring for this role, by one of these:
1. They posted this job themselves ("We're hiring a backend engineer... DM me"), unless their title or post shows they are a recruiter,
   HR or an agency (then Recruiter).
2. The post or the job page names them as the hiring manager or the person the role reports to ("you will report to Priya").
3. LinkedIn's "Meet the hiring team" box for this job (from Exa's copy of the job page, or a screenshot the user pasted).
4. Someone at the company names them in a reply (a peer's answer): proof "Named by <who> in a reply".
A title alone never makes someone the hiring manager: not "founder", "founding team", "head of", "lead" or "manager". Without a
confirmation, step 4 (ask peers) applies. A peer with the same title as the job is a colleague to ask or a referrer, not the hiring
manager. At an MNC, never a director for an analyst job.

## How many
- **Startup, confirmed hiring manager:** the hiring manager (pitch), plus the poster if they are a recruiter at the company (recruiter
  note), plus at most one other recruiter if none posted: 1 to 2 people.
- **Startup, no confirmed hiring manager:** 2 peers (the peer ask), plus the poster if they are a recruiter at the company: 2 to 3
  people. When a peer names the hiring manager, that person is added and pitched (one more).
- **MNC:** one recruiter (the poster if a recruiter posted it) and up to 2 referrers in the same function in India: 1 to 3 people.
- **Agency:** the posting recruiter only: 1 person.
- **Size unknown:** as a Startup, plus one recruiter: 2 to 3 people.
Gather about 10% more people than you need across the round, so a bounced email can be replaced.
Prefer, at equal fit: the person who posted the job; someone from the user's college or a past company (say so in Notes, and the message
may say so, because it is true); someone in India for an India job.

## Write
One row per person in the People tab: Name, Title, Contact as, LinkedIn link (only a real `linkedin.com/in/` address), Proof, Status
"To contact". Then hand over to find-email and carry on (write, resume, send) without asking. Report in one line: who will be contacted (name, title)
and how many were left out.

## Rules (every JOBSOR skill keeps these)
- **Debug log:** if the profile says "Debug log: on", log every step of this skill as `skills/round/references/debug-log.md` says.
  Each person checked writes one row: Step "Find people", Item the person or the job, Tool, Input (search words), Result (OK / Empty /
  Hidden / Failed), Why (for example "poster is a job-sharing page", "Hunter: no result").
- Never invent a person, a title, a connection or a reason. Never write "we met" or "X suggested" unless the user said so.
- Never log in to LinkedIn and never open linkedin.com pages; read LinkedIn only through Exa's copy or Firecrawl's post reader.
- Never try to get past a "not a robot" check on any website; skip that page.

## Autopilot and short replies (every JOBSOR skill)
- Never stop to ask the user to pick a job or a person, or to approve a message. Carry on through the next steps the round would take.
  Ask only when nothing can be done without an answer.
- Replies show only the results, precise and short: a table is fine for results (jobs, people, messages sent); no plans, no filler, no explanations unless asked.
