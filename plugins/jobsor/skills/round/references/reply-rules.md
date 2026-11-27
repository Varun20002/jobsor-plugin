# Reading a reply

Ported from the JOBSOR website (`lib/mail.ts` classifier, `lib/mail-domain.ts`, MASTER Journey 7). Check in this order; the first that
fits wins. Read only the new part of a reply: drop the quoted earlier mail ("On ... wrote:", "-----Original Message-----", lines starting
with ">"), so the user's own words are never read as theirs.

| # | It is | When | Do |
|---|---|---|---|
| 1 | Not a person | From a no-reply, alerts, notifications, digest, newsletter address, or a job site's bulk mail (naukri.com, instahyre.com, cutshort.io, wellfound.com, hirist, foundit.in, internshala.com); an unsubscribe link with a "view in browser" or "manage preferences" footer; "You applied to ..." receipts; LinkedIn "accepted your invitation" | Ignore. Follow-ups go on |
| 2 | Auto-reply | "Out of office", "automatic reply", "thank you for your interest", "thank you for applying", "application has been received" | Ignore; never answer it. Follow-ups go on. If an out-of-office gives a return date, move the next follow-up to the day after it |
| 3 | Bounce | From mailer-daemon or postmaster, naming one of the user's sent addresses | Bounced: clear the address, try the next format or person |
| 4 | Do not contact | "stop messaging", "do not contact", "don't email me", "remove me", "not interested in this role", "not hiring" | Person: Do not contact on every job. Job: Rejected if it is about this job |
| 5 | Rejection | "regret to inform", "not moving forward", "application unsuccessful", "decided to go with other candidates" | Job: Rejected. Stop follow-ups. No draft |
| 6 | Asks for the resume | "share/send/attach your resume or CV" | Job: Replied. Reply draft with the resume attached |
| 7 | Asks CTC | "current/expected CTC or salary", "salary expectation" | Job: Replied. Reply draft with the reply facts |
| 8 | Asks notice | "notice period", "when can you start/join" | Job: Replied. Reply draft with the reply facts |
| 9 | Referral done | "submitted/made the referral", "referred you" | Job: Replied. Thank-you draft; tell the user to apply only through the referral link |
| 10 | Hiring manager named | A clear sentence: "<Name> is the hiring manager", "the hiring manager is <Name>", "<Name>, our hiring manager"; "reach out to <Name>" counts only if the same reply speaks of the hiring manager or who leads the role | Add <Name> with proof "Named by <sender> in a reply" (and the email if written right after the name). Pitch them; thank the sender |
| 11 | Wants a call | "schedule/book an interview or call", "your availability", "time slot" | Job: Interview. Reply draft in the same thread, saying yes to the call; times only if the user gave them, otherwise a clear blank "[your free times, IST]". Tell the user to fill the blank and send |
| 12 | Anything else from a person | A real reply that fits none of the above | Job: Replied. Stop follow-ups. Tell the user to read it; no guessing what it means |

Any real reply (4 to 12) from **anyone at the company**, not only the person written to, stops **all** outreach to that company, on every
job at it: no new messages, no drafts, no follow-ups. In the same round every Messages row for that company with Status "Draft ready"
becomes "Stopped (company replied)" and its Gmail draft is deleted, every People row there with Status "To contact" or "Draft made"
becomes "Stopped (company replied)", and every job there gets Status Replied (or Interview, Rejected). The reply draft for the user is
still made.

Reply drafts use only the profile's reply facts (current and expected CTC, notice period, city, relocation) and confirmed facts. If the
reply asks for something the profile does not have, the draft leaves a clear blank ("[your expected CTC]") and the report tells the user.
