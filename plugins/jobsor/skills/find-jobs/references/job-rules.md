# Which jobs to keep, and the Match score

Ported from the JOBSOR website (`lib/relevance.ts`, `lib/eligibility.ts`, `docs/MATCH_PLAN.md`, `lib/domain.ts` scam rules).
A job the user pasted is never hidden: apply the rules, show the warnings, keep it.

## The title is only a wide first gate
Job titles mean different things at different companies, so the **description decides the fit, not the title**. The title only removes
jobs that are plainly in another field.
- **Keep** a job when its title **or** the first lines of its description name the user's field, any of their roles, any of their
  related titles (profile, "What I want"), or the kind of work their confirmed facts show. Same work under another name counts: a title
  the user never typed is kept when the description is that work.
- **Hide** (reason "another field") only when both the title and the description are clearly another line of work, for example a
  sales, support, HR, accounting or warehouse job for a user who does none of these, or a software job for a user in finance.
- When unsure, keep it: read the description and let the Match decide.

## Hide the job when (write the reason)
1. **Another field** (above).
2. **Too senior.** Levels: Intern 0, Entry 1, Mid 2, Senior 3, Lead 4, Executive 5. Judge the job's level from the years and duties in its
   description first; use title words (senior, sr, staff, principal, lead, head, director, VP, chief, AVP above; junior, associate, entry,
   graduate, fresher, trainee below) only when the description says neither. Hide when the job is two or more levels above the user, or
   asks for more than the user's years + 2 ("minimum 4 years" for a user with 1).
3. **An internship** when the user is Entry or above.
4. **Outside the user's cities.** Hide when the job is in a city the user did not pick; when it is remote only outside India ("Remote - US",
   "EMEA only", "Remote, Ireland"); or remote when the user did not add "Remote". Bangalore = Bengaluru, Gurgaon = Gurugram, Bombay =
   Mumbai, New Delhi and Delhi NCR = Delhi. "Location not stated" is kept and noted.
5. **A never-contact company** (current employer and others in the profile).
6. **IT services** (TCS, Infosys, Wipro, HCLTech, Tech Mahindra) unless the user asked for them.
7. **A scam:** asks for payment, a deposit or a registration or training fee; "Telegram tasks" or WhatsApp-only hiring; "earn per day/task"
   or pay far above normal; asks someone to interview on another's behalf; hiring from a personal Gmail/Yahoo/Outlook address in the post.
8. **A post that is not hiring** (it mentions the role but offers no job).
9. **Older than 3 days.** Only jobs posted in the last 3 days are kept (posted date, or the alert mail's date when that is all there is).
   A job with no date at all is hidden too. Hidden jobs are counted with the reason "older than 3 days" and never added.

## Warnings (keep the job, show the warning)
- **College rule** ("IITs, NITs and IIITs only", "tier-1 only") and the user's confirmed college is not one: "This job limits applicants
  (IIT). Your confirmed college, X, may not qualify." Take 25 off the Match.
- **A stretch:** the description asks for 2 or more years more than the user has, or its duties are clearly one level above them (leading
  a team, owning a whole function). Judge the level from the years and duties in the description, never from a title word alone ("Manager",
  "Owner", "Lead", "II" mean different things at different companies). The Match is capped at 60, and the gap line will be used in messages.
- **Other limits** the post states (a degree, a notice period, a location to relocate to): shown as "Check who can apply: <the rule>".

## Match N / 100 (from the description only)
Score three parts separately and write each in Notes, for example "Work 30/45, Must 28/40, Level 15/15", so every run scores the same way.

- **Work fit (45):** from the description, list the 3 to 5 main things the person in this job does day to day. For each, check the user's
  confirmed fact lines: **done** (a fact shows they did this kind of work; name it, F3), **close** (similar work, a smaller version, or the
  same work with other tools), **new**. Score 45 x (done + half of close) / number of things.
- **Specific must-haves (40):** only the specific requirements the post says are required: tools, languages, methods, certifications,
  licences, degrees, a named kind of experience. **Soft or generic words never count** ("communication", "analytical", "team player",
  "ownership", "fast learner", "agile mindset", "MS Office", "problem solving"). For each: **met** (a fact shows it; name it), **partly**
  (a fact shows something close), **missing**. A general skill never proves a specific one (Python does not prove Django). Score
  40 x (met + half of partly) / number of must-haves. If the post names no specific must-have, this part takes the same fraction as work fit.
- **Level and years (15):** 15 when the years and duties asked fit the user; 8 when they are a stretch; 12 when the post says nothing about
  either. When the user has not set level or years, use the years since their last degree. The script `skills/round/scripts/jobsor.py score` works this out from the years; use its number. Only 15, 12 or 8 are allowed.
- No description: no Match. Never score a job from its title, company or a snippet; it stays "Can't read" until a reader or the
  user's screenshot gives the description.
- A short post is not punished for being short: score what it says.
- Role, city and recency only decide what is kept and the order, not the number. Recency breaks ties: posted in the last 24 hours
  first, then the last 3 days.

## Worked examples (made-up jobs and users from different fields, to keep scoring the same)
1. **Title hides the fit.** User: backend developer, 1 year, built REST APIs in Go and ran them on AWS. Job: "Platform Associate"; the
   description: build and run internal APIs in Go, keep AWS services healthy, on-call. Title is not the user's role, but the description
   is their work: kept. Work 4 of 4 done = 45; must-haves Go met, AWS met, Kubernetes missing = 27; level fits = 15. **Match 87.**
2. **Title matches, work does not.** User: data analyst, SQL and dashboards. Job: "Data Analyst"; the description: chase overdue invoices,
   update the billing sheet, call customers. Work 1 of 4 close = 6; must-haves "Excel" met, "Tally" missing = 20; level fits = 15.
   **Match 41.** The title alone would have passed it.
3. **A title word is not the level.** User: UX designer, 1 year. Job: "Product Designer II", 1 to 3 years, design flows in Figma and run
   usability tests. Years fit, so no stretch and no cap. Work 3 of 3 done = 45; Figma met, usability testing met = 40; level 15. **Match 100.**
4. **Generic words do not inflate.** User: sales associate. Job: "Junior Analyst"; must-haves "communication, analytical mind, MS Office,
   team player" and nothing specific; daily work: build financial models in Excel for loan files. Work 0 of 3 = 0; no specific
   must-haves, so this part takes the work-fit fraction = 0; level 15. **Match 15.**
5. **A real stretch.** User: entry-level mobile developer, 1 year. Job: "Android Developer", 4+ years, leads two developers. Years are
   3 more than the user has: stretch, Match capped at 60 even if the skills all fit.
