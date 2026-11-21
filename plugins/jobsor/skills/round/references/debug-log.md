# Debug log (off unless the profile says "Debug log: on")

Setup never adds this line and never asks about it. It is for the person who runs or builds JOBSOR, to see every step of every round.
When the profile has no such line, or it says off, write none of this.

## Where
Two tabs in the tracker. If a tab is missing, add it with its header row first.

**"Debug steps"**: one row for every step, in the order it happened.

| Column | What goes in it |
|---|---|
| Time | India time, `YYYY-MM-DD HH:MM` |
| Round | The round's start time (the same for every row of one round), or "by hand: <skill>" |
| Step | One of: Alert mail, Post search, Apify, Indeed, Read job, Filter, Score, Dedupe, Add job, Route, Find people, Find email, Check email, Write, Resume, Send, Draft, Follow-up, Reply check, Bounce check |
| Item | What it was about: the Gmail id, a job (J007 or "Title at Company" before it has an id), a person (P005), a message (M004) |
| Tool | The tool or connector called (Firecrawl scrape, Firecrawl search, Exa fetch, Exa search, Apify, Indeed, Hunter finder, Hunter verifier, Vibe, Gmail search, Gmail send, Gmail draft, Python), or "none" |
| Input | The address read, the search words or the name looked up, short |
| Result | OK, Failed, Empty, Skipped, Hidden, Merged, Can't read |
| Why | One plain line: what was found or why it failed ("robot check on naukri.com", "asks 3-5 yrs", "Hunter: no result", "Match 45, under 50") |
| Credits | Credits this call used when the tool says so, as "Firecrawl 2" or "Hunter 1"; blank if none or not known |

**"Debug emails"**: one row for every alert email the round opened.

| Column | What goes in it |
|---|---|
| Mail id | The Gmail id |
| Sender | The sender's address |
| Mail date | The date of the mail |
| Read in round | The round's start time |
| Jobs inside | How many job links the mail held |
| Added | Job ids added from it |
| Merged | Job ids it matched that were already in the tracker |
| Hidden | Each hidden job as "Title at Company: reason", separated by "; " |
| Can't read | Job ids no reader could open |
| Finished | Yes when every job in it is handled; No when the round stopped part way (the next round adds a new row for the rest) |

## Rules
- A row is written for every step, including the ones that found nothing and the ones that were skipped (say why).
- Write the rows in batches (at the end of each part of the round), not one call per row.
- Never put mail text, message text or resume text in these tabs: only ids, links, titles, companies, names, tool names and one-line reasons.
- A round in quiet hours writes one row: Step "Reply check", Result "Skipped", Why "quiet hours".
