# Reading job-alert emails

Every rule here was learned from real alert mail (JOBSOR website, `lib/alert-mail.ts`, `docs/FEED_SOURCES.md`).

## Which mail
Search Gmail for mail from the last 3 days from these senders (only the portals the profile lists):

| Portal | Sender ends with | A job link looks like |
|---|---|---|
| Naukri | `@naukri.com` (for example naukrialerts@naukri.com) | `naukri.com/jd/job-listings-...` or `naukri.com/job-listings-...` |
| LinkedIn | `@linkedin.com` (jobalerts-noreply@linkedin.com) | `linkedin.com/jobs/view/<id>` or `linkedin.com/comm/jobs/view/<id>` |
| Wellfound | `@wellfound.com` | `wellfound.com/jobs/...`, `/l/...`, `/company/<name>/jobs/...` |
| Instahyre | `@instahyre.com` | `instahyre.com/job...` |
| Cutshort | `@cutshort.io` | `cutshort.io/job/...` |
| Hirist | `@hirist.tech` or `@hirist.com` | `hirist.tech/j/...` |
| Foundit | `@foundit.in` | `foundit.in/job...` |
| Internshala | `@internshala.com` | `internshala.com/job/detail/...` or `/internship/detail/...` |
| Jack & Jill | `@jackandjill.ai` | `jackandjill.ai/job...` |

Read each mail once (its id goes in the Seen tab once every job in it is handled). **Every job link in the mail is taken**, not only the
first: a digest of 6 jobs gives 6 jobs, each filtered and scored on its own (at most 30 a mail).

## Which links are jobs
- A link on the portal's own site whose address looks like the job link above is a job, whatever its text.
- A link whose text is a job button ("Apply", "Apply now", "View job", "Open job", "View details", "Learn more", "Apply on company site")
  or a job title may go through a tracking address; follow it to the real page.
- Never jobs: unsubscribe, preferences, settings, privacy, terms, help, app store, social links, profile, login, dashboard.

## Title, company, city
- **LinkedIn:** each job is one link whose text is "Title Company · City (On-site)". The title ends at the last role word (Manager,
  Analyst, Engineer, Developer, Designer, Lead, Associate, Specialist, Consultant, Architect, Scientist, Owner, Executive, Intern...); the
  company is what follows it; the city is after "·". If the company is not in the link text, it is on the line under the link.
  Reduce the link to `https://www.linkedin.com/jobs/view/<id>/`.
- **Naukri:** the address is `/jd/job-listings-<title>-<company>-<city>-<years>-<id>`. Read title, company, city and years from it.
- **Jack & Jill:** "Title (Company)" or "Title (Company - description)".
- **Others:** "Title at Company", "Title - Company" or "Title | Company"; otherwise the job's own page says.

## Date (write how it is known in the Posted column)
- **Naukri:** the job id at the end of the address starts with the day it was created, as ddmmyy (for example `...-151126000123` was
  created on 15 Nov 2026). This matched the page's own date on 5 of 5 real jobs. Posted = that date, "Naukri job id".
- **LinkedIn:** never open the page. Posted = the alert mail's date, "alert date, not checked".
- **Wellfound, Cutshort, Internshala:** their job pages carry a real posted date; read the page with Firecrawl. "page date".
- **Instahyre, Foundit:** their pages refuse automated reads. Keep the job; Posted = the alert's date, "alert date, not checked".
- **Jack & Jill:** the alert's date, "alert date, not checked".
- Kept only when the date is within the last 3 days. Older or undated: hidden ("older than 3 days"), not added.

## Description
Alert mails carry no description. For each kept job that passes the filters (at most 10 a round): search for the same job on the
company's own careers page or hiring system (Workday, Greenhouse, Lever, Ashby, SmartRecruiters, Workable, Keka, Darwinbox), then one
general search "<title> <company> careers"; read what you find with Firecrawl. If that fails, go through every reader in the find-jobs skill ("Describe it"). If none can read
the job, never score it as an estimate: Status "Can't read", and the user is asked for a screenshot or the job's text.
