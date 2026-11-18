---
name: find-people
description: Find the right people to contact for a job in the JOBSOR tracker (hiring manager, founder, recruiter, referrer), each with proof they work at the company now. Use when the user asks "who is the hiring manager", "find people for this job", "who should I write to at this company", pastes a hiring-team screenshot, or when the JOBSOR round reaches a job with no people yet.
---

# Find people, with proof

Read the JOBSOR profile and the job's row first. The route skill has set Size (Startup, MNC, Agency) and who to look for; if it has not,
run route first. Then search in the order below and **stop as soon as the right person is found with proof**: a hiring manager or founder
at a startup; the recruiter and up to 2 referrers at an MNC; the posting recruiter for an agency.

**Before anyone is written to the People tab, apply `references/proof-rules.md`.** A person goes in only with a proof they work at this
company now and no contradiction. Unsure means left out. Never relax the proof to fill the list. Write the proof in plain words in the
Proof column.

## Order of search

1. **The hiring post itself.** If the job came from a LinkedIn or X post, the poster comes first, plus anyone the post names ("reach out to
   Priya", "DM me", "my team"). Their own hiring post for this job is a proof.
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
4. **Ask a peer (startups only).** Still no hiring manager: find 1 or 2 people in the same team (same function, with proof they work there
   now) and add them with Contact as "Peer (to ask)". The write skill gives them the peer ask: "Do you know who the hiring manager for this
   role is?" It is never a pitch and never asks for a referral. When a peer replies with a name, the round adds that person with the proof
   "Named by <peer> in a reply" and drafts the pitch to them. At an MNC the peer step is not used.
5. **Then pitch.** Only once the right person is found does the write skill write to them.

## Who counts as the hiring manager
**The person whose own post hires for this role** ("We're hiring a Product Analyst... DM me") counts as Hiring manager, even when their
title is not known, unless their title or post shows they are a recruiter, HR or an agency (then Recruiter). Otherwise:
same function as the job **and** more senior than the job (lead, manager, head, director, VP, founder over an entry or associate role). A
peer with the same title ("Product Manager" for a "Product Manager" job) is a colleague to ask or a referrer, not the hiring manager.
At an MNC, never a director for an analyst job.

## How many
Startup: the hiring manager or a founder, plus at most one recruiter; peers only when step 4 is needed (at most 2). MNC: one recruiter and
at most 2 referrers. Gather about 10% more people than you need across the round, so a bounced email can be replaced.
Prefer, at equal fit: the person who posted the job; someone from the user's college or a past company (say so in Notes, and the message
may say so, because it is true); someone in India for an India job.

## Write
One row per person in the People tab: Name, Title, Contact as, LinkedIn link (only a real `linkedin.com/in/` address), Proof, Status
"To contact". Then hand over to find-email and carry on (write, resume, send) without asking. Report in one line: who will be contacted (name, title)
and how many were left out.

## Rules (every JOBSOR skill keeps these)
- Never invent a person, a title, a connection or a reason. Never write "we met" or "X suggested" unless the user said so.
- Never log in to LinkedIn and never open linkedin.com pages; read LinkedIn only through Exa's copy or Firecrawl's post reader.
- Never try to get past a "not a robot" check on any website; skip that page.

## Autopilot and short replies (every JOBSOR skill)
- Never stop to ask the user to pick a job or a person, or to approve a message. Carry on through the next steps the round would take.
  Ask only when nothing can be done without an answer.
- Every reply to the user is at most 5 short lines. No tables, no lists of what you will do, no explanations unless asked.
