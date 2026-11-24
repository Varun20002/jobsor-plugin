# Debug log (off unless the profile says "Debug log: on")

Setup never adds this line and never asks about it. It is for the person who runs or builds JOBSOR, to see every step of every round.
When the profile has no such line, or it says off, write none of this.

## Where
Three tabs in the tracker. If a tab is missing, add it with its header row first.

**"Debug steps"**: one row for every step, in the order it happened.

| Column | What goes in it |
|---|---|
| Time | India time, `YYYY-MM-DD HH:MM` |
| Round | The round's start time (the same for every row of one round), or "by hand: <skill>" |
| Step | One of: Plan (one row per round: the window and the due list), Alert mail, Post search, Apify, Indeed, Read job, Filter, Score, Dedupe, Add job, Route, Find people, Find email, Check email, Write, Check, Resume, Send, Draft, Follow-up, Reply check, Bounce check |
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

**"Debug jobs"**: one row for **every job seen** in the round, from any source, kept or not.

| Column | What goes in it |
|---|---|
| Round | The round's start time |
| Source | Alert mail (with its Gmail id), LinkedIn post, X post, Apify, Indeed, Company board, Pasted |
| Title | The job title as shown |
| Company | The company |
| Link | The job's link (or the post's link) |
| Posted | The posted date and how it is known |
| Read via | The reader that gave the description (Firecrawl, Exa, company page, Apify, Indeed, job site), or "Can't read" with the readers tried |
| Gate | Kept, or Hidden with the rule (another field, too senior, city, older than 3 days, never-contact, IT services, scam, not hiring) |
| Match | The three parts and the total ("Work 30/45, Must 28/40, Level 15/15 = 73"), blank when hidden before scoring |
| Decision | Added as J0xx, Merged into J0xx (why), Hidden (why), Waiting (cap reached) |



## Rules
- **Every round writes debug rows; no exceptions.** A round that writes none is not finished. The busiest rounds (new-jobs windows) matter
  most: never skip the log to save time.
- **Write as you go:** after each part of the round (replies, follow-ups, alert mails, each source, each job's people, emails, messages,
  sends), write that part's rows before starting the next part, so a round that stops part way still leaves its trail.
- **One row per item, never a summary:** one row per search or tool call (its words, how many results, credits), one per alert mail
  (in "Debug emails" too), one per job seen (in "Debug jobs" too), one per person checked, one per email address tried, one per message
  written and one per send. "4 alerts already seen" is four rows, one per mail id.
- **Minimum rows a part must leave** (when the part runs): Reply check and Bounce check: one row each. Follow-up: one row per message due
  or not due. Alert mail: one row per mail. Each job source (post search, X, Apify, Indeed, company board): one row per call. Read job,
  Filter, Score: one row per job. Route: one row per job (size, source, call). Find people: one row per person checked plus one per search.
  Find email: one row per address tried. Write: one row per message (type, length in words, checks passed). Send: one row per send (the
  To address, Gmail id, Result).
- **Skipped parts still get a row** with the reason ("3 PM window already run", "Apify: once a day, ran at 09:57", "cap of 50 reached").
- **Credits:** fill the Credits column whenever the tool reports a cost (Firecrawl, Apify, Hunter).
- **Check before the Log row:** count this round's debug rows and write the count at the end of the round's Log row ("debug: 34 rows").
  If the count is 0, or a part that ran has no rows, write the missing rows first.
- Write the rows in batches (one write per part), not one call per row.
- Never put mail text, message text or resume text in these tabs: only ids, links, titles, companies, names, tool names, numbers and
  one-line reasons.
- A round in quiet hours writes one row: Step "Reply check", Result "Skipped", Why "quiet hours".
- Never read these tabs back in a round; only append. To count this round's rows, count what you wrote.
