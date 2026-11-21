# JOBSOR changes that touch the user's setup

Newest last. Each entry is one version. **Step** means the update skill runs it with the user; **Note** means it is only told in one
line (the new rule already works by itself). A version with no entry changed only rules that work by themselves.

A profile with no "Plugin version" line was made before 0.2.8: treat it as 0.2.7.

## 0.2.5 and 0.2.7
- Note: LinkedIn jobs through Apify (optional; the user's own Apify account, about $0.15 a day at most) and Indeed jobs (optional,
  free) are new job sources. Connect them on the plugin's Connectors tab if wanted. Skip this note if both are already connected.

## 0.2.8
- Step **gmail-check**: Gmail now comes from Claude's own Gmail connector, not one inside the plugin. Do one harmless Gmail read (list
  labels, or search one message from the last day; show nothing). If it fails, tell the user: on claude.ai open Settings, then
  Connectors, find Gmail, click Connect and sign in. Then try once more.

## 0.2.9
- Step **resume-links**: links are now taken from the resume itself. If the profile's Links section is empty or has blanks, ask the
  user to attach the resume PDF once more, take every link out of it as the setup skill says, show them, and fill only the
  blanks after the user says ok. If the Links section is full, skip this step silently.

## 0.2.10
- Step **alerts**: find the connected Gmail address, check which of the 9 alert senders reached it in the last 30 days, save the list of
  sites in the profile, and tell the user in one line which sites to turn on alerts for (one alert per target role, sent to that address).

## 0.2.11
- Note: `/jobsor:update` exists. After each JOBSOR update, type it once; it runs only what is new.

## 0.2.14
- Step **resume-source**: each job now gets its own one-page tailored resume. If the profile has no "Resume source" section, read the
  resume file named in Links (or ask the user to attach the PDF once), and save it line for line in a new "Resume source" section as the
  setup skill says, leaving out lines the user removed from the confirmed facts. In Cowork or Claude Code, copy the PDF into the
  `JOBSOR/` folder if it is not there and note its full path.
- Step **resume-column**: add the column "Resume" at the end of the tracker's Jobs tab (header only).
- Note: say "go ahead with J004" to pick a job under Match 50; the next round writes for it and tailors the resume.

## 0.2.15
- Step **resume-summary**: tailored resumes now keep the professional summary. If the resume has a summary and the profile's Resume
  source has no "Summary" part, read the resume file named in Links (or ask for the PDF once) and add the summary word for word at the top
  of Resume source. If the resume has no summary, skip this step silently.

## 0.2.16
- Step **autopilot**: JOBSOR now runs on its own and keeps replies short. If the profile's Sending mode is "drafts", ask once, in one
  line: "Let JOBSOR send for you, up to 20 a day, 9 AM to midnight? (ok / keep drafts)". Save the answer. Guessed emails stay drafts.

## 0.2.18
- Step **cloud-round**: the round can now run in the cloud with the laptop closed. If this Claude has cloud scheduling (`list_triggers` /
  `create_trigger`, as on claude.ai) and there is no cloud "JOBSOR round": if the profile and tracker are files on the laptop, copy them
  to Claude Docs (or Google Drive) first; then create the cloud round as the setup skill says. Then tell the user in one line to turn off
  the old desktop "JOBSOR round" (Scheduled in the sidebar), so it never runs twice. If there is no cloud scheduling here, say in one
  line: "Open claude.ai and type /jobsor:update there to run JOBSOR with the laptop closed." Skip if a cloud round already exists.

## 0.2.20
- Note: Vibe Prospecting (optional, Settings > Connectors) is a backup for finding people and emails, used only after Exa, Firecrawl
  and Hunter. Skip this note if it is already connected.

## 0.2.21
- Step **send-default**: sending is now the default. If the profile's Sending mode is "drafts", set it to "send for me" (20 a day, 9 AM to
  midnight) and say so in one line; the user can say "drafts" to go back. Guessed emails and replies stay drafts.

## 0.2.22
- No step to run. Jobs: every job in an alert email is now read (not only the first), a job page that will not open goes through every
  reader (Firecrawl, Exa, the company page, Apify, Indeed, other job sites) and, if none works, is marked "Can't read" with a request for
  a screenshot instead of a guessed Match; the job search runs every round (the LinkedIn post search stays three times a day).

## 0.2.23
- No step to run. A hidden debug log for whoever runs or builds JOBSOR: with the profile line "Debug log: on", every round writes each
  step to "Debug steps" and each alert email to "Debug emails" in the tracker. Setup and update never add it.

## 0.2.24
- Step **related-titles**: matching now works for any field and is decided by the job description, not the title. If the profile's
  "What I want" has no "Related titles:" line, add one under Roles: 4 to 8 other titles used for the same work as the user's roles, from
  their resume. Do not ask; say in one line "Added related titles: ...; change them any time."

## 0.2.25
- No step to run. Only jobs posted in the last 3 days are kept; older or undated jobs are hidden ("older than 3 days") instead of
  being added as "Listed earlier" (a job the user pastes still goes ahead).

## 0.2.26
- No step to run. Job sources: searches use the roles plus the related titles; X posts are searched with Firecrawl (x.com only, recent)
  instead of Exa; Apify and Indeed add "entry level" for Intern or Entry users; Indeed (the plugin's or Claude's own connector) keeps only
  jobs posted in the last 3 days.

## 0.2.27
- No step to run. Startup or MNC: the line is now 1,000 people (listed companies are always MNC); the size comes from one Google-style
  search of the company's LinkedIn page; an unknown size is never assumed (contact the hiring manager and a recruiter); placement firms
  hiding the client are Agencies. Existing jobs keep their label.

## 0.2.28
- No step to run. People and email: the job poster is always checked first; at a startup the order is hiring manager, then founder,
  then a peer ask; a recruiter poster is contacted together with the hiring manager or founder; the company's website comes from its
  LinkedIn page (never a guessed domain); when no address is found or checked, the best guess is built and labelled; the address sent
  is exactly the one in the tracker, and any difference is logged.

## 0.2.29
- No step to run. A hiring manager is contacted only when confirmed (their own post, named in the post or job page, LinkedIn's hiring
  team box, or named by someone at the company); a title alone (founder, founding team, head) is never enough. Without a confirmed
  hiring manager, 2 peers are asked who it is (a founder only when no peer can be found).

## 0.2.30
- Step **referral-template**: in the profile's Templates, change the Referral ask's title line to "Referral ask (MNC referrers; at a
  startup, peers once the hiring manager is confirmed):" and its ask line to "Would you be open to referring me for {role} ({job_id}),
  or sharing this with the hiring team?". Do not ask; say so in one line.
- More people per job: startup with a confirmed hiring manager, the hiring manager + 1 recruiter + 2 peers (refer or share); startup
  without one, up to 10 peers asked who the hiring manager is + the posting recruiter; MNC, up to 3 recruiters + up to 10 referrers;
  agency, the posting recruiter only if the agency is legitimate.

## 0.2.31
- No step to run. New profiles start with a daily cap of 50 emails (the most allowed), since more people are contacted per job. An
  existing profile keeps its cap; the user can say "set my daily cap to 50".

## 0.2.32
- No step to run. Messages that are ready are sent in the same run, back to back, with no 50-second wait between them.

## 0.2.33
- No step to run. Ready messages are sent in the same run with a random 1 to 5 second wait between two sends.
