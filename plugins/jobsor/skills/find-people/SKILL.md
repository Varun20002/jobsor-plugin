---
name: find-people
description: Find the right people to contact for a job in the JOBSOR tracker (hiring manager, founder, recruiter, referrer), each with proof they work at the company now. Use when the user asks "who is the hiring manager", "find people for this job", "who should I write to at this company", pastes a hiring-team screenshot, or when the JOBSOR round reaches a job with no people yet.
---

# Find people, with proof

Read the JOBSOR profile and the job's row first. The route skill has set Size (Startup, MNC, Agency) and who to look for; if it has not,
run route first. Then search in the order below and **stop as soon as the right person is found with proof**: a confirmed hiring manager
at a startup (or, without one, the peers to ask); the recruiters and referrers at an MNC, up to the numbers in "How many"; the posting recruiter for an agency.

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
   If the post or the job page says where to send applications (an email address, even a shared one like hiring@ or careers@), add that
   address as a contact with Contact as "Company inbox" and send it the pitch with "Hi {company} team,". It does not count toward the
   people numbers.
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
   - **Exa people search first** (free): `web_search_exa` with `category:people` and plain words, about 10 to 15 results a search, one
     search at a time (Exa's free plan refuses several at once). Each result is a profile with the current job marked "(Current)", the
     city, the school and past jobs. Searches, as the job needs them:
     - peers and referrers: `category:people <job title or function> at <company>, <city> India`;
     - recruiters: `category:people Talent Acquisition recruiter at <company>, <city> India, hiring <function> roles`;
     - the user's college and past companies first: `category:people <company> <city> <function>, studied at <user's college>` and
       `... previously at <user's past company>`;
     - startups: `category:people founder of <company>` and `category:people head of <function> at <company>`.
     Keep a person only when their profile shows this company as "(Current)" (proof: "Current job on profile: <title>, <company>") and
     passes `references/proof-rules.md` (in India for an India job; not a namesake company). An address they show on their own profile
     is a `published` email. Run more searches (other titles in the same function, a second city) until the numbers in "How many" are
     reached or nothing new comes back.
   - Headline searches with Exa (without `category:people`) only as a backup: `"<role or function> at <company>"`,
     `"talent acquisition" "<company>" India`. Read results as people only when the line is theirs.
   - The company's own team or about page (`/team`, `/about`, `/company`), read with Firecrawl.
   - Hunter's people at the company's domain, if Hunter is connected (a Hunter record alone is not proof; it needs a public line that
     agrees).
   - **Last, the wide backup: Vibe Prospecting**, only if it is connected (optional) and only when Exa, Firecrawl and Hunter found
     nobody fitting, or Hunter is out of credits: `match-business` for the company, then `fetch-entities` for prospects at it by title
     (hiring manager's function, founder, recruiter or talent acquisition, India). At most 1 search a job, to save its small free credits.
     A Vibe record alone is not proof: it needs a public line that agrees (post, headline, team page). If it says no credits, skip it
     for the rest of the day.
4. **Startup with no confirmed hiring manager: ask peers.** Never guess the hiring manager from a title. If steps 1 to 3 did not find a
   person confirmed as hiring for this role (see "Who counts as the hiring manager"), do not pitch anyone: ask up to 10 peers who the
   hiring manager is. A founder, a "founding team" member or a head of the function is **not** assumed to be the hiring manager; they are
   pitched only when confirmed. If no peer in the same team can be found (a very small company), ask a founder the same question
   instead of pitching them.
   **Ask peers (startups only).** Find up to 10 people in the same team (same function, with proof they work there
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
- **Startup, confirmed hiring manager:** the hiring manager (pitch) + one recruiter (the poster if a recruiter posted it) + 2 peers in
  the same team (Contact as "Referrer"; they get the referral ask: refer me, or share this with the hiring team): up to 4 people.
- **Startup, no confirmed hiring manager:** up to 10 peers in the same team (the peer ask: who is the hiring manager?) + the recruiter
  who posted, if any: up to 11 people. When a peer names the hiring manager, that person is added and pitched, and the remaining peers
  are not followed up.
- **MNC:** up to 3 recruiters (the poster first if a recruiter posted it; then recruiters whose title or posts cover this kind of role,
  in India) + up to 10 referrers (same function, in India, user's college or past company first): up to 13 people.
- **Agency:** the recruiter who posted, only if the agency is legitimate (it has its own website and LinkedIn company page, and the post
  asks for no fee or deposit): 1 person. Otherwise nobody, with the reason in Notes.
- **Size unknown:** as a Startup.
Take people in this order of preference until the number is reached: the person who posted the job; someone from the user's college
or a past company (say so in Notes, and the message may say so, because it is true); someone in India for an India job; then the rest.
If fewer people can be found with proof, contact the ones found; never relax the proof to reach the number.
Gather about 10% more people than you need across the round, so a bounced email can be replaced.

## Write
One row per person in the People tab: Name, Title, Contact as, LinkedIn link (only a real `linkedin.com/in/` address), Proof, Status
"To contact". Then hand over to find-email and carry on (write, resume, send) without asking. Report in one line: who will be contacted (name, title)
and how many were left out.

## Rules
- **Shared rules:** follow `skills/round/references/shared-rules.md` (read it once per run; a round has already read it).
- **Debug rows:** each person checked writes one row: Step "Find people", Item the person or the job, Tool, Input (search words), Result (OK / Empty /
  Hidden / Failed), Why (for example "poster is a job-sharing page", "Hunter: no result").
- Never invent a person, a title, a connection or a reason. Never write "we met" or "X suggested" unless the user said so.
- Never open linkedin.com pages; read LinkedIn only through Exa's copy or Firecrawl's post reader.
