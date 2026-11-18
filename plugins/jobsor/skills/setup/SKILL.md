---
name: setup
description: Set up JOBSOR for a job seeker. Use when the user types /jobsor:setup, sends their resume to start JOBSOR, says "set me up", or wants to change their JOBSOR profile (roles, cities, facts, sending, alerts). Builds the profile and tracker every other JOBSOR skill reads.
---

# Set up JOBSOR

Setup turns the user's resume and a few answers into two files every JOBSOR skill reads first:
1. **"JOBSOR profile"**: a document. Layout in `references/profile-template.md`.
2. **"JOBSOR tracker"**: a spreadsheet with tabs Jobs, People, Messages, Seen, Log. Columns in `references/tracker-columns.md`.

It ends with a scheduled task, "JOBSOR round", so the work runs without the user.

If a profile already exists, read it first and change only what the user asks; never start over without asking.

## Steps (fast: two messages from the user, then everything runs by itself)

Setup is quick and leads straight into autopilot. Ask nothing that can be read from the resume, the inbox or a sensible default.

1. **Get the resume** (if it is not attached yet): one line, "Attach your resume PDF (or paste it) and I'll set everything up."
2. **Read it yourself, silently:**
   - Split it into numbered **fact lines** (each role, project, result, skill, degree), in the user's own words, numbers exactly as written.
   - Take every link out of it yourself, including links hidden behind words (PDF: `pypdf` `/Annots` `/URI` or `pdfplumber`
     `page.hyperlinks`; DOCX: its relationships file). Never ask for links; never guess one.
   - Save the resume line for line (summary included) as the profile's **Resume source**; tailored resumes use only it.
   - Fill the rest from the resume with defaults: roles = the 2 or 3 titles it fits, level and years from the dates, cities = the city on
     the resume (plus "Remote"), company kinds = startup, product MNC, GCC, never contact = current employer.
   - Find the connected Gmail address and check which alert senders reached it in the last 30 days (Naukri, LinkedIn, Wellfound,
     Instahyre, Cutshort, Hirist, Foundit, Internshala, Jack & Jill). Never show mail text.
3. **One confirm message** (the only real question), short, in this shape:
   ```
   Facts I'll use (only these, ever):
   1. ... 2. ... (one short line each)
   Roles: A, B · Level: Entry · Cities: Bengaluru, Remote · Skip: <current employer>
   Sending: send for me, up to 20 a day, 9 AM to midnight (or say "drafts")
   Reply "ok", or fix anything (for example "remove 4, add Pune").
   ```
   Any line the user removes is removed from the Resume source too. "ok" means everything as shown. **Sending is "send for me" only if
   the user replied "ok" to that line or chose it; "drafts" if they said drafts.** Guessed (unchecked) emails always stay drafts.
4. **Then do everything without asking again:** write the files, create the schedule, run the first round now.

Never ask for sample messages, a writing voice, template changes, reply facts (CTC, notice period; ask only later, when a reply needs
them) or anything already shown. Every user gets the same templates and voice from `references/profile-template.md`.

## Write the files

- Keep both files **online**, so the round can run in the cloud with the laptop closed: the **Claude Docs** connector (a doc and a
  sheet) first, else the **Google Drive** connector (a Google Doc and a Google Sheet). Only if neither is there, use a folder `JOBSOR/`
  with `profile.md` and `tracker.xlsx` (Cowork or Claude Code), and then the round needs the computer on.
- Nothing else needs saving: tailored resumes are built fresh from the profile's Resume source in each round (resume skill).
- Fill the profile from `references/profile-template.md`, copying the voice and templates exactly as written and the "Plugin version:" line (the `version`
  in this plugin's `.claude-plugin/plugin.json`). Create the tracker with the exact tab and
  column names in `references/tracker-columns.md`, empty except the header rows, and the Log tab's first row: today's date, "Setup done".

## The scheduled task

Create it right away (the user only clicks to approve if Claude asks). **Prefer a cloud schedule**: it runs on Anthropic's servers, so
it keeps going with the laptop closed and the report reaches the phone.
- **Name:** JOBSOR round
- **When:** every hour (the round does nothing between midnight and 9 AM India time and searches for new jobs only three times a day, so
  most runs are short).
- **Instructions** (self-contained, so a fresh cloud run needs nothing else): `Run the JOBSOR round (/jobsor:round). Profile: <profile
  link>. Tracker: <tracker link>.`
Where:
1. **Cloud (best):** if this Claude has cloud scheduling tools (for example `create_trigger` / `list_triggers`, as on claude.ai), create
   the round there, hourly. First check `list_triggers` so there is never a second JOBSOR round.
2. **Desktop (only if there is no cloud scheduling):** the desktop app's scheduled task (Scheduled > New task > Set up manually > name
   "JOBSOR round", the instructions above, Hourly > Save). Tell the user in one line: "This one runs only while your computer is on;
   set JOBSOR up once on claude.ai to run it with the laptop closed."
Each round's report reaches the user as a Claude notification (phone and computer); nothing else is needed.

## Finish

Run the first round now (round skill), without asking. Then reply with only the results, for example:
```
Done. Profile, tracker and hourly round are set; JOBSOR now runs by itself.
First round: 6 jobs, 4 emails sent, 2 drafts (guessed addresses).
To do once: turn on Naukri and LinkedIn alerts for Product Analyst to you@gmail.com.
Files: <link>
```
Name only alert sites that are missing. No other explanations.

## Rules (every JOBSOR skill keeps these)

- Write only what the user confirmed about themselves. Never invent a fact, a number, a skill, a company or a warm connection.
- Never log in to LinkedIn and never message anyone on LinkedIn for the user.
- Never send an email unless the user turned sending on; otherwise leave a draft.
- Never copy the text of the user's mail into any file; keep only links, titles, companies, names and dates.
- Never try to get past a "not a robot" check on any website; skip that page.
- Plain, short words. Never stop to ask the user to pick a job or a person or to approve a message: carry on.
- Replies show only the results, precise and short: a table is fine for results (jobs, people, messages sent); no plans, no filler, no explanations unless asked.
