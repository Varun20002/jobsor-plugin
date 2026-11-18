---
name: round
description: Run one JOBSOR round - check replies and bounces, stop jobs where the company replied, draft replies for the user, send due follow-ups, find new jobs and people, write and send or draft new messages, then report. Use when the scheduled task says "Run /jobsor:round", or when the user says "run JOBSOR", "check my replies", "do the round".
---

# The JOBSOR round

Read the profile and the whole tracker first. Note the time in India (IST, UTC+5:30) and the last round's time (last row of Log).

**Quiet hours:** between 12 midnight and 9 AM India time, do nothing, write nothing, and end with "Quiet hours, nothing done." (A round
the user starts by hand runs anyway, but sends nothing in quiet hours.)

## 1. Replies and bounces (every round)
Search Gmail for mail received **since the last round** (not just the last 2 hours; if there is no last round, the last 3 days):
- from any address in the People tab, **and**
- from any address at the company domain of a job the user has contacted (Status Contacting or Contacted). A personal mail domain (Gmail,
  Outlook, Yahoo, Rediffmail, iCloud, Proton, Zoho and the like) never counts as "the company".
- plus bounce notices (`from:mailer-daemon` or `from:postmaster`) that name an address in the People tab.
Leave out the user's own mail, job-alert mail and mail already handled (its Gmail id is in a Messages row or a Notes line).
Classify each with `references/reply-rules.md` and act:
- **A real reply** from anyone at the company: the job's follow-ups stop at once. Set the job's Status (Replied, Interview, Rejected), the
  person's Status Replied, and a dated note (one line, your words, never the mail's text). If they ask something (resume, CTC, notice,
  availability), write a **reply draft** for the user with the write skill, using only the reply facts and confirmed facts, as a Gmail
  draft in the same thread. **Never send a reply.**
- **Someone else at the company replied** (not the person written to): add them to People with the title from their signature, or
  "not known"; Contact as is left blank unless their title says it. Never guess a role.
- **The hiring manager is named** in a reply (by a peer or anyone): add that person to People with the proof "Named by <who> in a reply",
  find their email, and write the pitch. Write the peer a short thank-you draft.
- **"Not hiring", "not interested", "stop", "do not contact":** that person is "Do not contact" on every job; follow-ups to them stop.
- **A bounce:** the message is "Bounced", the person's email is cleared with a dated note; try the next email format (find-email) or the
  next person.
- **Auto-replies** (out of office, "thank you for applying", "application received") and LinkedIn notices: ignore; follow-ups go on.

## 2. Follow-ups due
For every Sent message whose Next follow-up date has come, check `skills/write/references/followups.md` rules (via the write skill): no
reply from the company, fewer than 3 follow-ups so far, 9 AM to 12 midnight in the recipient's time (any day of the week). Write the follow-up with a new opening fact,
then hand to send.

## 3. New jobs (only three times a day)
Only in the first round after 9 AM, after 3 PM and after 9 PM India time (check the Log for whether this window already ran):
run find-jobs. For each new job with Status Found and Match 50 or more (best first, at most 5 a round): route, find-people, find-email,
write, then send (draft or send, by the profile). Jobs under 50 stay Found for the user to choose.

## 4. Pasted work
Any job the user added by hand since the last round (Status Found, Source "Pasted link") goes through the same steps whatever its Match.

## 5. Log and report
Write one Log row: time and one line of counts ("2 replies (Acme asks for a call), 1 bounce replaced, 3 follow-ups, 4 new jobs, 5 drafts,
0 sent"). Then the report to the user:
- If nothing changed: change nothing else and end with exactly "No new replies."
- Otherwise a short summary, replies first, then what the user must do (send drafts, answer a reply, check a guessed address).
- If the user connected **Bird**, also send this summary to the user's **own** WhatsApp number from the profile (only theirs, never anyone
  else's). If Bird fails, say so in the report.

## If the schedule is missing
If this round was started by hand and there is no "JOBSOR round" scheduled task, tell the user how to add it: Scheduled > New task > Set up
manually > name "JOBSOR round", prompt "Run /jobsor:round.", Hourly > Save.

## Never
- Never reply to a recruiter, a peer or anyone at a company; only draft for the user.
- Never send outside 9 AM to 12 midnight India time or above the cap.
- Never copy mail text into the tracker; one line in your own words.
- Never log in to LinkedIn.
