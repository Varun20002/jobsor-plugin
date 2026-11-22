---
name: send
description: Send JOBSOR messages from the user's Gmail, or leave them as Gmail drafts with the resume attached, within the user's daily cap and hours, then log each one and report. Use when the user says "send them", "make the drafts", "send my JOBSOR messages", or when the JOBSOR round has messages marked Draft ready.
---

# Send or draft

Read the profile's Sending section (mode: send for me unless it says drafts; daily cap, hours, guessed emails) and the Messages rows with Status "Draft ready".

## Before each message (skip it, with the reason in Notes, if any check fails)
1. **Stop rules:** no reply from anyone at the company since the last message (check Gmail now, not only the tracker); the person is not
   "Do not contact"; the company is not on the never-contact list; the job is not Replied, Interview, Rejected, Skipped or No response.
2. **Address:** `published` or `checked`, or `guessed (not checked)` only when the profile allows sending to guesses. Otherwise it stays a
   draft whatever the mode.
3. **Not twice:** no message of the same type to the same person for the same job was already sent (look at Messages and at Gmail's Sent).
4. **Cap and hours** (send mode): fewer than the daily cap sent today (count the Messages rows Sent today), and the time is between 9 AM and
   12 midnight India time.

## The address is the tracker's address
Use the People tab's Email exactly as written, character for character (dots, hyphens, case). Never retype or "clean" it. After
sending (or making a draft), read the sent message's To address from Gmail. If it differs from the People tab's Email, write the address
actually used into the People tab's Email and add a dated note "Sent to <address>, tracker had <old>"; log it in the debug log with
Result "Failed" and Why "address changed".

## Drafts (only if the profile says drafts, or the address is a guess)
Create a Gmail draft to the person with the subject and body, the resume attached, and for a follow-up as a reply in the same thread.

**Which resume:** the job's tailored PDF, made by the resume skill in this same run (run it first if this job has none yet). If no PDF
can be made, attach the original resume file from the profile and add the note "original resume attached". Follow-ups are replies in
the same thread and attach nothing. Filename `<Name>_Resume_<Company>.pdf`, type `application/pdf`. How to attach:
- In Cowork or Claude Code: a file reference, `sha256:<hash>:<full path>` (hash from `shasum -a 256 "<path>"`).
- On claude.ai (web, mobile, cloud schedule): the file's base64 as the attachment content (`base64 -w0 "<path>"`; the PDF is a few KB).
The same attachment goes on a message sent in send-for-me mode.
Set Status "Draft ready", Gmail id = the draft id. Tell the user how many drafts are waiting and that they send them from Gmail.

## Check every message before it goes out (code, not judgement)
- Before each send or draft, write `message.json` (type, subject, body, facts = the profile's Confirmed facts and Resume source, job_text =
  the job's row (role, must-haves, notes) plus the description read this round and the person's post if the message uses it, name,
  linkedin, first_name) and run `python3 -I <this skill's folder>/scripts/check_message.py message.json`.
- Pass: send. Fail: fix exactly the problems it prints (the write skill's rules), run it again; at most 3 tries, then leave the message as
  a draft with the problems in Notes. Never send a message that failed, and never edit the script's output.
- Every run writes a debug row (Step "Check", Item the message id, Result Pass/Fail, Why the problems).
- If Python cannot run at all, send nothing that round and write a debug row "Check: Python unavailable".
- The daily cap: count today's Messages rows with Status Sent (the round's own count); the hook's file count does not survive between
  cloud runs.

## Send for me
- Send every ready message in the same run, one after another, up to the daily cap and the hours. Wait a random 1 to 5 seconds between
  two sends (different each time; on a computer, `python3 -c "import random,time; time.sleep(random.uniform(1,5))"`). After each send,
  write the row (Status "Sent", Sent time, Gmail id, Next follow-up = the next day); write the rows in batches if there are many.
- After every 20 sends, and at the end: search Gmail for bounce notices (`from:mailer-daemon` or `from:postmaster`, newer than today) that
  name one of today's addresses. For each bounce: the message becomes "Bounced", the person's email is cleared with a dated note, and the
  person goes back to find-email for the next format, or is replaced by the next person found for that job.
- Stop at the cap; the rest wait for tomorrow (say so).

## Report
One line of counts (sent, drafts, bounced, skipped), then at most 2 lines the user must act on. Nothing else.

## Never
- Never send outside the hours, above the cap, or when the user chose drafts. Sending is the default: do not leave a checked or published address as a draft.
- Never answer a recruiter or anyone who replied; replies are drafts for the user (the round makes them).
- Never send from any address other than the user's own Gmail.

## Rules
- **Shared rules:** follow `skills/round/references/shared-rules.md` (read it once per run; a round has already read it).
