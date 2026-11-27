# JOBSOR plugin: where things stand (27 Nov 2026)

Read `CLAUDE.md` first (rules, layout, release steps). This page is the state of play and what is next. Decisions and their reasons are
in `DECISIONS.md`; research notes in `RESEARCH.md`. Update this page at the end of every session.

## Versions
- **Plugin 0.2.48** is pushed and installed on the owner's Mac. The zip was sent to the owner; **whether he uploaded 0.2.47 / 0.2.48 on
  claude.ai is not confirmed** (0.2.46 was uploaded on 27 Nov). Check by asking him, or by the version a cloud round reports.
- **Email checker 0.2.0** runs on the owner's Mac (LaunchAgent `com.jobsor.emailchecker`), relay Worker `jobsor-email-checker`
  (workers.dev) deployed; the owner added it on claude.ai as a custom connector ("Email checker"), and a call from Claude worked.

## What the last versions did (newest last)
| Version | What changed |
|---|---|
| 0.2.42 | Code keeps the round's rules: `jobsor.py plan` (sources due per window: morning 9-15, afternoon 15-21, night 21-24), Indeed hook (no level words), stop hook (due sources must run), `score` script (Level only 15/12/8, stretch cap 60), `people` script (targets), agency with a named client is routed twice |
| 0.2.43 | Stop hook only in real rounds (the round skill ran, or the chat starts with "Run the JOBSOR round" or "/jobsor:round") |
| 0.2.44 | `people --job` keeps a log; the stop hook refuses to end a round while a job sent a NEW message has a people run not "done" |
| 0.2.45 | Every guessed address is checked before sending; label `checked (accept-all)`; profile line "Send to guessed, unchecked emails" retired; send hook refuses a new email to an unchecked address (reads the transcript: a verifier call with a valid/accept_all status, or the tracker row read as published/checked) |
| 0.2.46 | A connected `verify_email` tool (the owner's email checker) is tried before Hunter |
| 0.2.47 | The checker's reason and warnings (daily limit, offline, may be blocked) go into the debug log, the Log row and the report |
| 0.2.48 | Up to 5 email formats checked per person, at most 3 of them on Hunter |

## Measured facts worth knowing
- 24 Nov rounds: 19 messages sent, 0 replies by then; 10 Hunter-checked addresses all delivered; 2 of 10 unchecked guesses bounced
  (Zepto), which led to 0.2.45.
- Owner's Hunter free plan: 32.5 of 50 credits used between 20 and 25 Nov (resets on the 20th). A check costs 0.5, a find 1.
- Reacher on the owner's Mac (25 Nov): 13 of 13 known results right (10 delivered = safe, 2 bounces = invalid, 1 made-up = invalid);
  5 accept-all domains = "cannot tell", same as Hunter. Port 25 is open on the owner's home internet.
- Hunter free plan: `List-Job-Titles` and `Preview-People` are free (first name + last initial, title, an email-verification flag, no
  email, no city). Apollo free plan: people search API refused ("not included in your Free plan").

## Open items (in order)
1. **Confirm the uploads** (0.2.47, 0.2.48 on claude.ai). Nothing for the user to run: every entry since 0.2.43 is "No step to run".
2. **Check the next real rounds** in the tracker's debug tabs:
   - each job sent a new message has a `jobsor.py people` row ending Done (0.2.44);
   - no new email went to a `guessed (not checked)` address; Find email rows say which checker answered ("Checker: valid" etc.);
   - any checker warning appears in the Log row and the report.
3. **Not tested live:** the checker's "daily limit" and "may be blocked" warnings (unit tests only); the Mac after a full restart (the
   checker restarts at login; a service restart was tested and kept the same connector address); a cloud round using the checker.
4. **Known gaps from the 24 Nov review, not fixed:** the stop hook counts any Firecrawl call as "post search" (the X search was
   skipped once); a Hirist alert mail waited 5 hours; one score was not run through the script; Hunter credits were spent on a job
   under Match 50.
5. **Ideas discussed, not approved to build:**
   - Free phone numbers: numbers published in hiring posts and Hunter's free `phone_number`, in two new People columns, listed in the
     report for the user to check in Truecaller/GPay by hand. Never automate Truecaller or GPay. Owner said "leave this" for now.
   - WhatsApp: best fit is a ready-to-send `wa.me` link in the report (the user taps Send). A linked-WhatsApp connector (like the main
     project's OpenWA) is possible but breaks WhatsApp's rules and risks bans; Meta's official API does not fit cold outreach.
   - Publishing the email checker to users: a rented server with port 25 (about EUR 4-5 a month), a key per user, limits, a privacy
     note; only after revenue. Sharing the owner's own connector address with 5-10 friends is acceptable for a test (400 checks a day
     shared; ~10-30 per user a day).

## Cloud test routine
RemoteTrigger routine `trig_0139bWPgHvvgWpYUtoRdddpV` (disabled) was used for hook tests in the cloud. `RemoteTrigger run` ignores a
message body; it runs the stored prompt. Check the cloud's plugin version before any cloud test. Ask the owner before using it.
