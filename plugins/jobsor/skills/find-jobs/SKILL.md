---
name: find-jobs
description: Find fresh jobs for a JOBSOR user in India and add the ones that fit to their tracker. Use when the user says "find jobs", "any new jobs", pastes a job link, a LinkedIn or X post link, or a hiring-team screenshot, or when the JOBSOR round reaches its job search.
---

# Find jobs

Read the JOBSOR profile and tracker first (setup made them; if there is no profile, run setup first). Then collect jobs from the sources
below, in this order, filter and score them with `references/job-rules.md`, and add the ones that fit to the tracker's Jobs tab.

## Sources, in order

1. **What the user pasted** (a job link, an apply form, a LinkedIn or X post link, a screenshot).
   - Never filter these out: the user chose them; just show the Match and any warning.
   - A job page: read it with Firecrawl (scrape). A LinkedIn job link: never open linkedin.com yourself; reduce it to
     `linkedin.com/jobs/view/<id>` and read Exa's copy of it (Exa search or fetch for that address), else find the same job on the
     company's own careers page.
   - A LinkedIn post link: read the whole post with Firecrawl. The poster and anyone the post names are people for the find-people skill.
     Open each link inside the post once: a job page is read, a form is saved as the Apply link, anything else is left.
   - A screenshot: read it yourself. A "Meet the hiring team" screenshot gives names and titles for the job named in its caption or the
     message; if no job is named, ask which job it is for. Never guess.
2. **Job-alert emails in Gmail** (only the senders the profile lists). Follow `references/alert-mail-rules.md` exactly. Read each alert
   mail once: skip any whose Gmail id is in the Seen tab, then add its id. Keep only links, title, company, city and date; never copy the
   mail's text anywhere.
   Once a week (the first round on Monday), check each alert site in the profile: if one has sent nothing in 7 days, tell the user once
   ("No Naukri alerts reached <connected address> this week; check the alert is on and sent to this address").
3. **Hiring posts from the last 24 to 48 hours.**
   - **LinkedIn's own post search first** (through Firecrawl; no LinkedIn login, LinkedIn is never opened by us). For each target role (up
     to 3), one call: `firecrawl_scrape` with an `alexandria` body `{"provider": "harvestapi", "capability": "linkedin/search-posts",
     "options": {"search": "hiring <role> <city>", "postedLimit": "24h", "sortBy": "date"}}` (the first city in the profile; add the second
     city only if the first gave nothing useful). About 2 Firecrawl credits a call. Each post comes with its text, its time, and the author's
     name, headline and profile link.
   - **Then Exa**, for X posts and as a backup when the LinkedIn search fails or finds nothing: one search like
     `"hiring" "<role>" "<city>" site:x.com` (and `site:linkedin.com/posts` only as the backup).
   - **Keep a post only if** it is really offering a job (it says "we're hiring", "we are looking for", "apply", "DM me", "share your
     resume", "referrals open"), names the company, is for one of the user's roles, and is no older than 48 hours. LinkedIn's search is
     fresh but noisy; **drop**: job digests and lists of many roles from job-sharing pages ("20 new roles this week", "daily job drop",
     "jobs bulletin"); people looking for a job ("open to work", "looking for my next role", "seeking opportunities"); posts that name no
     company; roles outside the user's role families.
   - The poster is the first person to contact. Their headline, when it names the company, is their proof of working there; a recruitment
     agency or a job-sharing account is a recruiter, not the hiring manager. Read the links in the post as in step 1.
4. **Companies the user named** (target companies in the profile). Look the company up in `references/boards.json` (company name to
   careers board address, India openings count). If it is there, read that board with Firecrawl; if not, search "<company> careers" once
   and read the careers page. Never read the whole boards list in a round: it is a lookup for named companies only.
5. **LinkedIn jobs through Apify**, only if the user connected Apify (optional; it runs on the user's own Apify account and credits).
   Once a day, in the first round after 9 AM: for each target role (up to 3), `call-actor` with actor `curious_coder/linkedin-jobs-scraper`,
   input `{"keywords": "<role>", "location": "<first city>, India", "datePosted": "past24Hours", "limitPerSource": 25, "scrapeCompany": true}`
   and, in `callOptions`, `maxTotalChargeUsd: 0.07`; then read the run's items (`get-dataset-items`). About $0.002 a job, so at most about
   $0.15 a day. No LinkedIn login. Each job gives the title, company, place, posted time, description and, when LinkedIn shows one, the
   person who posted it: that person is the first one for find-people (proof: "Posted this job on LinkedIn"). Reduce the link to
   `linkedin.com/jobs/view/<id>` so it matches the same job from an alert email. Run this source **after** the alert emails (source 2),
   so jobs the alerts already brought are recognised by their LinkedIn job id.
6. **Indeed or Jobs and Careers**, only if the user connected them: one search per target role and city (for Indeed, location as
   "<city>, India"). Indeed's connector is free (the user's own Indeed sign-in), gives salary when listed and the apply link, and its job
   details call gives the full description. **India check:** if two Indeed searches in a row return no job located in India, stop using
   Indeed for this user, note it in the Log tab, and tell the user once ("Indeed's connector returned no India jobs, so JOBSOR skips it").

## Then, for every job collected

1. **Describe it.** An alert job has no description: find the company's own page for it (one Exa search on the hiring systems with the
   title and company, then one general search), and read it with Firecrawl. At most 10 such look-ups a round. If a page shows a "not a
   robot" or human check (Naukri, Instahyre, startup.jobs often do), skip that page; never try to get past it.
2. **Date it.** Keep the date and how it is known (see `references/alert-mail-rules.md`). Jobs older than 3 days, or with no date, go in
   with Status "Listed earlier" and are never drafted for, unless the user pasted them.
3. **Filter it** with `references/job-rules.md`: role family, level and years, city or India remote, never-contact companies, IT
   services (hidden unless the user asked for them), scams. A job that fails a rule is not added; count it under "hidden" with the reason.
4. **Score it**: Match N / 100 as in `references/job-rules.md`. Write the must-haves met and missing.
5. **Dedupe** against the tracker: the same company and role (or the same job id, or the same link) is one job. A company-board copy
   wins over an alert copy (it has the real description and date). An Apify copy of a job that already came from a LinkedIn alert or a
   hiring post is **not a new job**: merge it into the existing row and use it only to fill what is missing there (the description, the
   real posted date, the job poster's name). Count it in the report as "enriched", not as new.
6. **Add** at most 10 new jobs a round, best Match first, with Status "Found".

## Report

When the user ran this by hand (not inside a round), do not stop at the list: carry straight on with the round's steps for the jobs
with Match 50 or more, and for any pasted job (route, find-people, find-email, write, resume, send), then report once.

A table of the jobs, best first: Match, Job (role at company, as a link), City, What happened (emailed <name>, draft, no person found). **Every job's role is a clickable
link to the job page**, written as a Markdown link, for example `[Product Analyst at Razorpay](https://...)`, so the user can open the job
before going ahead. Use the job's own link from the tracker (the company or job-site page; for an alert-mail job, the job link from the
mail, never the mail itself). If a job has no link, write "(no link)" after it. Never show a link that was not read or found for that job. Then one line of counts (more found, hidden, emails sent or
drafted) and, only if needed, one line the user must act on (for example "add Naukri alerts for Product Analyst in Pune").

## Rules (every JOBSOR skill keeps these)

- Write only what the user confirmed about themselves. Never invent a fact, a number, a skill, a company or a warm connection.
- Never log in to LinkedIn and never open linkedin.com pages; never message anyone on LinkedIn for the user.
- Never send an email unless the user turned sending on; otherwise leave a draft.
- Never copy the text of the user's mail into any file; keep only links, titles, companies, names and dates.
- Never try to get past a "not a robot" check on any website; skip that page.
- Plain, short words.

## Autopilot and short replies (every JOBSOR skill)
- Never stop to ask the user to pick a job or a person, or to approve a message. Carry on through the next steps the round would take.
  Ask only when nothing can be done without an answer.
- Replies show only the results, precise and short: a table is fine for results (jobs, people, messages sent); no plans, no filler, no explanations unless asked.
