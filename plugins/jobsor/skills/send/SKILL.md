---
name: send
description: Send JOBSOR messages from the user's Gmail, or leave them as Gmail drafts with the resume attached, within the user's daily cap and hours, then log each one and report. Use when the user says "send them", "make the drafts", "send my JOBSOR messages", or when the JOBSOR round has messages marked Draft ready.
---

# Send or draft

Read the profile's Sending section (mode, daily cap, hours, guessed emails) and the Messages rows with Status "Draft ready".

## Before each message (skip it, with the reason in Notes, if any check fails)
1. **Stop rules:** no reply from anyone at the company since the last message (check Gmail now, not only the tracker); the person is not
   "Do not contact"; the company is not on the never-contact list; the job is not Replied, Interview, Rejected, Skipped or No response.
2. **Address:** `published` or `checked`, or `guessed (not checked)` only when the profile allows sending to guesses. Otherwise it stays a
   draft whatever the mode.
3. **Not twice:** no message of the same type to the same person for the same job was already sent (look at Messages and at Gmail's Sent).
4. **Cap and hours** (send mode): fewer than the daily cap sent today (count the Messages rows Sent today), and the time is between 9 AM and
   12 midnight India time.

## Drafts (default mode)
Create a Gmail draft to the person with the subject and body, the resume attached, and for a follow-up as a reply in the same thread.

**Which resume:** the job's tailored PDF (the Jobs **Resume** column). If it is blank, run the resume skill for the job first; if that
cannot make one, attach the original resume file from the profile and add the note "original resume attached". Follow-ups attach the
same file as the first message. Attach it as a file reference, never typed-out content: `sha256:<hash>:<full path>` (get the hash with
`shasum -a 256 "<path>"`), filename `<Name>_Resume_<Company>.pdf`, type `application/pdf`. The same attachment goes on a message sent in
send-for-me mode.
Set Status "Draft ready", Gmail id = the draft id. Tell the user how many drafts are waiting and that they send them from Gmail.

## Send for me
- One email at a time: send, write the row (Status "Sent", Sent time, Gmail id, Next follow-up = the next day), then wait about 50 seconds
  before the next. Never send several at once.
- After every 20 sends, and at the end: search Gmail for bounce notices (`from:mailer-daemon` or `from:postmaster`, newer than today) that
  name one of today's addresses. For each bounce: the message becomes "Bounced", the person's email is cleared with a dated note, and the
  person goes back to find-email for the next format, or is replaced by the next person found for that job.
- Stop at the cap; the rest wait for tomorrow (say so).

## Report
One line of counts (sent, drafts, bounced, skipped), then at most 2 lines the user must act on. Nothing else.

## Never
- Never send outside the hours, above the cap, or when the user chose drafts.
- Never answer a recruiter or anyone who replied; replies are drafts for the user (the round makes them).
- Never send from any address other than the user's own Gmail.

## Autopilot and short replies (every JOBSOR skill)
- Never stop to ask the user to pick a job or a person, or to approve a message. Carry on through the next steps the round would take.
  Ask only when nothing can be done without an answer.
- Replies show only the results, precise and short: a table is fine for results (jobs, people, messages sent); no plans, no filler, no explanations unless asked.
