# JOBSOR plugin: research notes

Findings that shaped decisions, so nobody repeats them. Newest last.

## Monid "job search" (25 Nov 2026)
- monid.ai/lp/job-search and github.com/monid-ai/monid (connector plumbing) + github.com/monid-ai/skills, skill `recruiter-email`.
- Monid has no data of its own: it resells Apollo, Hunter and a LinkedIn job reader with its own paid keys, per call.
- Their flow (about 7 calls, ~$0.09 a posting): read the LinkedIn job; domain from the LinkedIn company page (confirm a company by its
  LinkedIn link, not its name); Apollo people search (free) for recruiter titles and for leaders of the job's function, which shows a
  `has_email` flag; paid Apollo match only where `has_email` is true; for a hiring manager with no email, Hunter finder then Hunter
  verifier; accept-all = "not confirmed".
- Their "hiring manager" is a title guess with no proof. Their recorded runs: recruiter verified 2/2, hiring manager valid 1/2.
- Useful for JOBSOR: check for free before paying; title lists per function; rank recruiters (other functions lower); trust the
  verifier over the finder; read the team size. Not usable: Apollo's free plan blocks the people search API.

## Hunter and Apollo free plans (25 Nov 2026, owner's accounts, no credits used)
- Hunter Free: `List-Job-Titles` (team counts by department, titles) and `Preview-People` (first name + last initial, title, seniority,
  decision-maker flag, verification status of the email Hunter holds, no address, no city, no LinkedIn link) are free. `Reveal-Emails`
  costs 1 credit each. Data is "inferred", not proof of current employment.
- Apollo Free: `mixed_people/api_search` refused: "not included in your Free plan".

## Reacher email check from the owner's Mac (25 Nov 2026)
- reacherhq/check-if-email-exists v0.11.10, x86_64 macOS binary (no arm64 build; runs on Apple silicon). Port 25 open at home.
- 25 addresses from the tracker: 13/13 known results right; 5 accept-all domains "risky, catch-all" (same as Hunter); the 7 unchecked
  Zepto guesses all "safe". About 2-4 s a check; one catch-all check took 38 s (timeout set to 60 s).
- Earlier (28 Oct, main project `docs/SOURCES_TESTED.md`): Cloudflare and Google Cloud VMs block port 25; Mimecast-protected domains
  answered "unknown".

## How phone-number providers get numbers (27 Nov 2026, from knowledge, not tested)
- Crowd-sourced address books (Truecaller), contributor networks that trade free credits for shared contacts (Apollo, ContactOut,
  Lusha), public pages (resumes, company pages, hiring posts), data brokers. Free options for JOBSOR: numbers published in hiring
  posts, Hunter's free `phone_number`, Prospeo (about 10 credits a number on a small free plan). Main project code: `lib/phone-find.ts`.

## WhatsApp options (27 Nov 2026, from knowledge, not tested)
1. Meta's WhatsApp Business API: cloud-friendly but a business number, Meta-approved templates for first messages, paid; wrong fit.
2. Linked personal WhatsApp (WhatsApp Web protocol, e.g. OpenWA built in the main project, off): needs an always-on server holding
   each user's session behind a connector; against WhatsApp's rules, ban risk for messages to strangers, heavy privacy load.
3. `wa.me/<number>?text=...` links in the report: free, official, the user taps Send. Best fit.
