# Which jobs to keep, and the Match score

Ported from the JOBSOR website (`lib/relevance.ts`, `lib/eligibility.ts`, `docs/MATCH_PLAN.md`, `lib/domain.ts` scam rules).
A job the user pasted is never hidden: apply the rules, show the warnings, keep it.

## Hide the job when (write the reason)
1. **Not one of the user's roles.** The title must be in one of their role families, or contain a role they typed. Families (phrases, never
   loose words):
   - Product manager: product manager, associate/assistant product manager, product management, APM, product owner, product lead, PM.
   - Product analyst: product analyst, product analytics, growth analyst, product data analyst, product operations analyst.
   - Founder's office: founder's office, chief of staff, CEO's office, office of the CEO or founders, business or executive associate to the
     CEO or founder.
   - AI product builder: AI product manager/builder/engineer/lead/owner, GenAI product, AI builder, product engineer, founding product or
     engineer, LLM product.
   - Solutions engineer: solutions engineer, sales engineer, pre-sales engineer, customer engineer.
   - Forward deployed engineer: forward deployed, FDE, deployment strategist, deployed engineer.
   - Any other role the user typed: the title contains it as a phrase.
2. **Too senior.** Levels: Intern 0, Entry 1, Mid 2, Senior 3, Lead 4, Executive 5. Title words: senior, sr, staff, principal, lead, head,
   group, director, VP, chief, AVP mean above; associate, junior, entry, graduate, fresher, trainee, APM mean below. Hide when the job is two
   or more levels above the user, or asks for more than the user's years + 2 ("3+ years", "minimum 4 years").
3. **An internship** when the user is Entry or above.
4. **Outside the user's cities.** Hide when the job is in a city the user did not pick; when it is remote only outside India ("Remote - US",
   "EMEA only", "Remote, Ireland"); or remote when the user did not add "Remote". Bangalore = Bengaluru, Gurgaon = Gurugram, Bombay =
   Mumbai, New Delhi and Delhi NCR = Delhi. "Location not stated" is kept and noted.
5. **A never-contact company** (current employer and others in the profile).
6. **IT services** (TCS, Infosys, Wipro, HCLTech, Tech Mahindra) unless the user asked for them.
7. **A scam:** asks for payment, a deposit or a registration or training fee; "Telegram tasks" or WhatsApp-only hiring; "earn per day/task"
   or pay far above normal; asks someone to interview on another's behalf; hiring from a personal Gmail/Yahoo/Outlook address in the post.
8. **A post that is not hiring** (it mentions the role but offers no job).

## Warnings (keep the job, show the warning)
- **College rule** ("IITs, NITs and IIITs only", "tier-1 only") and the user's confirmed college is not one: "This job limits applicants
  (IIT). Your confirmed college, X, may not qualify." Take 25 off the Match.
- **A stretch:** the title is one level above the user, or asks for 2 or more years more than they have, or a plain "Manager" or "Owner"
  title for an Entry user. The Match is capped at 60, and the gap line will be used in messages.
- **Other limits** the post states (a degree, a notice period, a location to relocate to): shown as "Check who can apply: <the rule>".

## Match N / 100
- **Must-haves (85):** list the job's must-haves (skills, tools, experience it says are required, not "nice to have"). For each, check the
  user's confirmed fact lines: **met** (a fact shows it; name the fact, F3), **partly** (a fact shows something close), **missing**. A
  general skill never proves a specific one (Python does not prove Django). Score 85 x (met + half of partly) / number of must-haves.
  If the post names fewer than 3 must-haves, take at most two thirds of the 85 and call the Match an estimate.
- **Level (15):** 15 when the level and years asked fit the user; 8 when one is a stretch; 12 when the post says nothing about level or
  years; when the user has not set level or years, use the years since graduating.
- No description: score from the user's confirmed skills the title and snippet mention, and call it an estimate.
- Role, city and freshness only decide what is kept and the order, not the number. Freshness breaks ties: posted in the last 24 hours
  first, then the last 3 days.
