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
