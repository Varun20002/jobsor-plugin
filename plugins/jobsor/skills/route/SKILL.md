---
name: route
description: Decide, for a job in the JOBSOR tracker, whether the company is a startup, an MNC or a recruitment agency, and who to contact (hiring manager, founder, recruiter, referrer). Use when a JOBSOR job needs people, when the user asks "who should I contact for this job", or when the JOBSOR round reaches a new job.
---

# Startup or MNC, and who to contact

Ported from the JOBSOR website: MASTER decisions 9 and 38, Journeys 5 and 6, and the owner's rules on who to contact.

## 1. Size
**Find the size (one search almost always does it).**
1. **Confirm the company first:** take its website address from the job, the post or the careers link, so a company with the same name
   elsewhere is never used.
2. **One Google-style search of LinkedIn:** `firecrawl_search` with query `<company> LinkedIn company employees`,
   `includeDomains: ["linkedin.com"]`, `limit: 3`, `sources: ["web"]` (about 2 credits). The result for the company's own page
   (`linkedin.com/company/...`, matching the website or the name) shows "Company size: 501-1,000 employees" and often "View all N
   employees". Use the **Company size band**; if only "View all N employees" is shown, use N. If the search also returns a company
   record (employees, founded, headquarters), it confirms the same thing.
3. Only if that finds nothing: Exa `category:company <company>`, then one search for a funding article or its listing on a stock
   exchange. Run these one at a time (Exa's free plan refuses several at once).
4. If the search shows the company's website, write it in the job's Notes as "Website: <domain>".
5. Write the size, where it came from and the founded year in the Size column ("501-1,000 employees, LinkedIn company page, founded
   2014").

**Decide.**
- **1,000 people or fewer: Startup. Above 1,000: MNC.** A band that ends at 1,000 ("501-1,000") is a Startup; "1,001-5,000" and above is
  an MNC.
- **Listed on a stock exchange: MNC**, whatever the size.
- **Size still unknown** after the steps above (rare): never assume. Write "Size unknown" and contact both ways: the poster or hiring
  manager (as for a Startup) **and** a recruiter (as for an MNC).
- **Agency:** the post is by a staffing, recruitment, consulting-placement or overseas-placement firm and the client company is hidden or
  named only as "our client". Contact only the recruiter who posted it; no founders, no employees. If the client is named, route the job
  as the client company.
- **Debug log:** write one row for this step: the size, the source, the founded year and the call.

## 2. Who to contact

**Startup** (reach the person who decides):
- Hiring manager confirmed (own post, named in the post or job page, LinkedIn's hiring team box, or named by someone at the company; a
  title alone is never enough): the hiring manager (pitch) + one recruiter + 2 peers asked to refer or share with the hiring team.
- No confirmed hiring manager: up to 10 peers in the same team, asked only who the hiring manager is (a founder gets that question only
  when no peer can be found) + the recruiter who posted, if any.

**MNC** (referral and recruiter first; never hunt the hiring manager): up to 3 recruiters for this kind of role (the poster first) +
up to 10 referrers in the same function in India. No founders and no general HR at an MNC.

**Agency:** only the posting recruiter, and only if the agency is legitimate (own website and LinkedIn company page, no fee asked).

The exact numbers and order are in the find-people skill ("How many").

## 3. Match the function (owner's rules)
- The person who posted the job always comes first.
- Each job goes to leaders of its own function: engineering to engineering leaders (head of engineering, engineering manager), product
  to product leaders, design to design leaders, data and analytics to their heads, sales, marketing, finance or operations to theirs.
  When a job spans two functions, pick by what the description says the person does most.
- At an MNC, an analyst or junior job never goes to a director: use the recruiter or a manager in the same team.
- Contact a named team only if the job or its poster names it.
- University recruiters are not for this (unless the user is a student looking for campus roles).
- If nobody in the same function can be found, list people from other teams at the company, same city first, rather than nobody. This
  relaxes the team, never the proof that they work there.
- A managing director is not always a founder: write their real title.

## 4. Write it
Write Size in the Jobs tab, and in Next step: "Startup: find the hiring manager (data team)" or "MNC: recruiter, then 2 referrers".
Then hand over to find-people.

## Rules
- **Shared rules:** follow `skills/round/references/shared-rules.md` (read it once per run; a round has already read it).
