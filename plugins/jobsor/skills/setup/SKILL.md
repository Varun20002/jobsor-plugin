---
name: setup
description: Set up JOBSOR for a job seeker. Use when the user types /jobsor:setup, sends their resume to start JOBSOR, says "set me up", or wants to change their JOBSOR profile (roles, cities, facts, templates, sending, alerts). Builds the profile and tracker every other JOBSOR skill reads.
---

# Set up JOBSOR

Setup turns the user's resume and a few answers into two files every JOBSOR skill reads first:
1. **"JOBSOR profile"**: a document. Layout in `references/profile-template.md`.
2. **"JOBSOR tracker"**: a spreadsheet with tabs Jobs, People, Messages, Seen, Log. Columns in `references/tracker-columns.md`.

It ends with a scheduled task, "JOBSOR round", so the work runs without the user.

If a profile already exists, read it first and change only what the user asks; never start over without asking.

## Steps

Ask in at most 8 short messages. Group questions; offer sensible defaults the user can accept with "ok". Plain words.

1. **Resume.** Ask for it (pasted text or a PDF). Split it into numbered **fact lines**: each role, project, result, skill, degree, link.
   One fact per line, in the user's own words, with where and when. Keep numbers exactly as written.
   **Take the links out of the resume yourself; never ask the user to "send the links".** Collect every link in it: written addresses
   (linkedin.com/in/..., github.com/..., a portfolio or demo site, an email address) and links hidden behind words ("GitHub", "Demo",
   a project title, an icon). For a PDF, read the link addresses stored in the file, not just the visible text (with code tools:
   `pypdf` page annotations `/Annots` with `/A` `/URI`, or `pdfplumber` `page.hyperlinks`; a DOCX keeps them in its relationships
   file). Put each link on the fact line it belongs to (a project's demo on that project's line) and in the Links group. If a link's
   words are there but the address cannot be read, say so for that one link only and ask for just that one. Never guess an address.
2. **Confirm the facts.** Show the lines in groups (Work, Projects, Education, Skills, Links) and ask the user to reply "ok", or the
   numbers to remove, or corrections. A thin line gets one question ("Did you build the voice agent or support it?"). Only confirmed lines
   go into the profile. **These lines are the only things any JOBSOR message may say about the user.** Never add, round up, or improve a
   fact. If the user has no work experience, say so in the profile, so no message ever claims experience.
3. **What you want.** Target roles (any function; up to 5), level (Intern, Entry, Mid, Senior, Lead) and years of experience, cities
   (Indian cities; "Remote" if they want remote), pay floor in LPA (optional), company kinds they prefer (startup, product MNC, GCC; IT
   services are hidden unless they ask), companies to target (optional).
4. **Never contact.** Their current employer (pre-filled from the facts) and any other company they name.
5. **Links and resume file.** Show the links already taken from the resume (portfolio, GitHub, LinkedIn, demo per project) as part of the
   confirm step and ask only about ones that are missing or look wrong. The resume file to attach to emails (ask them to attach the PDF
   once; note where it is kept).
6. **Reply facts (optional, private).** Current CTC, expected CTC, notice period, current city, open to relocate. Say plainly: these are
   used only in draft replies JOBSOR prepares for them, never in a first message.
7. **Job alerts (JOBSOR's main job source).** JOBSOR reads job alerts only from the Gmail connected to Claude, so the alerts must arrive
   at **that same address**.
   - First find out which address is connected (read the Gmail profile, or one recent message's "To") and say it: "JOBSOR reads job
     alerts from <address>."
   - Then check that inbox for the last 30 days: which of these alert senders already arrive there: Naukri, LinkedIn, Wellfound,
     Instahyre, Cutshort, Hirist, Foundit, Internshala, Jack & Jill. Report found or missing for each. Never show mail text.
   - Tell the user to turn on alerts on **every** one of these sites they use (at least LinkedIn and Naukri), **one alert for each target
     role** in their cities (or India-wide), with the email set to the connected address. They are free. Give plain steps: sign in to the
     site, search the role and city, press "Set alert" / "Create job alert" (LinkedIn: the alert switch on the search results; Naukri:
     "Create job alert" on the search page), make sure the alert email is the connected address, repeat for each role.
   - If their sites send alerts to a different address, they either change the email on that site, or add a Gmail forwarding filter
     from the other inbox to the connected one. Never connect a second inbox for them.
   - Save the list of sites in the profile. The round's job search re-checks once a week and tells the user if a listed site has sent
     nothing for 7 days.
8. **How to send.**
   - **Drafts (default):** JOBSOR leaves Gmail drafts with the resume attached; the user presses Send in Gmail.
   - **Send for me:** JOBSOR sends by itself, 9 AM to midnight India time, up to a daily cap (default 20, never above 50).
   - **Guessed emails:** may JOBSOR send to an address built from the company's email format when no checker could confirm it? Default no
     (it stays a draft for them to look at).
   - **Their voice (optional):** paste 1 to 5 messages that once got a reply. Keep only the shape (opener, sign-off, how they ask), never
     facts from them.

## Write the files

- Use, in this order, whatever this Claude can write to: the **Claude Docs** connector (a doc and a sheet), the **Google Drive** connector
  (a Google Doc and a Google Sheet), or, in Cowork or Claude Code, a folder `JOBSOR/` with `profile.md` and `tracker.xlsx` (or one CSV per
  tab). Tell the user which one you used and give the links.
- The scheduled task must be able to read and write the same files. If you are unsure it can, say so and pick the first option.
- Fill the profile from `references/profile-template.md`, including the default templates. Create the tracker with the exact tab and
  column names in `references/tracker-columns.md`, empty except the header rows, and the Log tab's first row: today's date, "Setup done".

## The scheduled task

Propose one scheduled task the user approves:
- **Name:** JOBSOR round
- **When:** every hour (the round itself does nothing between midnight and 9 AM India time, and searches for new jobs only three times a
  day, so most runs are short).
- **Instructions:** `Run /jobsor:round.`
If you can create scheduled tasks here, propose it and let the user click Schedule. Otherwise tell them: Scheduled (left sidebar) > New
task > Set up manually > name "JOBSOR round", prompt "Run /jobsor:round.", Hourly > Save.

## Finish

Show a short summary: number of confirmed facts, roles, cities, sending mode, alert senders, where the files are, and the schedule. Then
offer the first win: "Paste a job link you care about, or say 'find jobs' and I'll run the first round now."

## Rules (every JOBSOR skill keeps these)

- Write only what the user confirmed about themselves. Never invent a fact, a number, a skill, a company or a warm connection.
- Never log in to LinkedIn and never message anyone on LinkedIn for the user.
- Never send an email unless the user turned sending on; otherwise leave a draft.
- Never copy the text of the user's mail into any file; keep only links, titles, companies, names and dates.
- Never try to get past a "not a robot" check on any website; skip that page.
- Plain, short words. One step at a time.
