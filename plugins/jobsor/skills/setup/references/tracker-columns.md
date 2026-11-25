# JOBSOR tracker: tabs and columns

Use these exact names. IDs are short and never reused: jobs J001, J002...; people P001...; messages M001...
Before writing, read the last filled row of the tab (to get the next ID and the sheet's current version); if a write is refused because
the sheet changed, read again and retry once.

## Jobs
| Column | What goes in it |
|---|---|
| Job ID | J001 |
| Found | Date and time found (India time) |
| Source | Pasted link, Naukri alert, LinkedIn alert, Wellfound alert, ..., LinkedIn post by <name>, X post by @<handle>, Company board, Indeed |
| Company | |
| Role | |
| Location | |
| Job link | The job's own page (LinkedIn links reduced to linkedin.com/jobs/view/<id>) |
| Apply link | A form or apply page, if different |
| Posted | Date, then how it is known: "page date", "Naukri job id", "alert date, not checked", "post date" |
| Size | Startup, MNC, Agency, Unknown (with the reason: "about 120 people (LinkedIn page)", "Workday careers page") |
| Match | Match N / 100 |
| Must-haves | "Met: SQL, Figma. Missing: Tableau" |
| Status | Found, Can't read, Listed earlier, Contacting, Contacted, Replied, Interview, Rejected, No response, Skipped |
| Next step | One plain line |
| Notes | Dated notes, newest last. Never mail text |
| Resume | Full path of this job's tailored resume PDF (blank until made; never remade once a message with it was sent) |

## People
| Column | What goes in it |
|---|---|
| Person ID | P001 |
| Job ID | |
| Name | |
| Title | |
| Contact as | Hiring manager, Founder, Recruiter, Referrer, Peer (to ask), Company inbox |
| LinkedIn | Profile link, if found |
| Proof | Why we know they work there now: "Posted about this job on 10 Nov", "Headline: PM at Acme", "On acme.com/team", "Named by P004 in a reply" |
| Email | |
| Email label | published, checked, checked (accept-all), guessed (not checked) |
| Status | To contact, Asked, Contacted, Replied, Bounced, Do not contact |
| Notes | |

## Messages
| Column | What goes in it |
|---|---|
| Message ID | M001 |
| Job ID | |
| Person ID | |
| Type | Pitch, Recruiter, Peer ask, Referral ask, Follow-up 1, Follow-up 2, Follow-up 3, Thank-you, Reply draft |
| Subject | |
| Opening fact | The relevant item the message opens with, with its date and link (blank when it has no opening) |
| Status | Draft ready, Sent, Bounced, Replied, Cancelled |
| Created | |
| Sent | Date and time sent (by JOBSOR or seen in Gmail's Sent) |
| Gmail id | Draft id or thread id |
| Next follow-up | Date, or blank when none is due |

## Seen
| Column | What goes in it |
|---|---|
| Mail id | Gmail message id of an alert mail already read (so it is read once) |
| Read on | |

## Log
| Column | What goes in it |
|---|---|
| When | Date and time of the round |
| What happened | One line: "3 new jobs, 2 drafts, 1 reply (Acme, asks for a call), 0 bounces" |
