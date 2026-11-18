---
name: resume
description: Make a one-page resume tailored to one JOBSOR job, from the user's own resume lines only, as a PDF that is attached to that job's emails. Use when the user says "tailor my resume for J004", "make the resume for this job", or when the JOBSOR round or send reaches a job that has no tailored resume yet.
---

# Tailor the resume for one job

The user's own resume, split into lines in the profile's **Resume source** section, is the only material. Tailoring picks, orders and
bolds those lines for this job. It never writes a new line, never rewords one, and never adds a skill, tool, number or title.

## When
- The round makes it for every job that goes on to messages (Match 50 or more, a pasted link, or a job the user chose), right after the
  first message is written and before send. It runs on the hourly schedule with no one watching; it never waits for the user.
- The user can ask for it on any job ("tailor my resume for J004").
- **Locked once used:** when a message with this job's resume was sent, never make it again for that job (the company already has it).
  Follow-ups attach the same file.

## Steps
1. **Read** the profile (Resume source, Links, About me) and the job's row (Role, Company, Must-haves, Notes) and its description (read
   the Job link once if needed).
2. **Pick and order** from the Resume source, section by section, in this order: Summary, Education, Experience, Projects, Skills,
   Achievements, Other (leave out an empty section).
   - Summary: if the resume has one, it goes first, under the name, word for word as a plain paragraph (`"text"` in the entry). If it has
     more than one, use the one that names the most must-haves or words from the job title. Bold at most 3 phrases in it, by the same
     rule as bullets. If the resume has no summary, leave the section out; never write one.
   - Every entry under Education and Experience stays. Inside each Experience entry, bullets that name a must-have or a word from the job
     title move first; the others keep their order.
   - Projects: keep the 1 or 2 that fit the job best (they name its must-haves or its kind of work). Project bullets keep their order.
     If a message for this job tells a project's story, that project stays.
   - Skills: matched skills first, then the rest, as written.
   - Bold at most 2 short phrases per bullet: a must-have the line already names, or a number already in the line. Mark bold with
     `**...**` in the JSON.
3. **Build** `resume.json` in the shape the script's header shows (name, contact from About me and Links with their URLs, sections,
   entries, bullets) and run:
   `python3 -I <plugin folder>/scripts/resume_pdf.py resume.json "<JOBSOR folder>/resumes/<Name>_Resume_<Company>.pdf"`
   (the plugin folder is the folder holding this plugin's `.claude-plugin`; make `resumes/` if it is missing).
   - "ok": done. "too long by N lines": drop the least relevant line (the last bullet of the weakest project first, then the last
     Experience bullet that names nothing from the job) and run again. Never shrink Education or the Summary.
4. **Check before saving:** every line in the JSON, with `**` removed, is a line of the Resume source, word for word. Nothing else. If a
   check fails, fix it; if it cannot pass, do not save, and the job uses the original resume file with a note.
5. **Save** the PDF's full path in the job's **Resume** column and a dated note: "Resume tailored: <projects kept>, <what moved first>".
   Delete `resume.json`.

## Where it cannot run
Making a PDF needs a folder JOBSOR can write and Python (Cowork and Claude Code have both). Where there is none (claude.ai chat with the
profile in Docs or Drive), do not try: the job uses the original resume file, and the report says once a day "Tailored resumes need Cowork
or Claude Code."

## Rules (every JOBSOR skill keeps these)
- Write only what the user confirmed about themselves. Never invent a fact, a number, a skill, a company or a warm connection.
- Never log in to LinkedIn and never message anyone on LinkedIn for the user.
- Never send an email unless the user turned sending on; otherwise leave a draft.
- Never copy the text of the user's mail into any file; keep only links, titles, companies, names and dates.
- Plain, short words. Never stop to ask the user to pick a job or a person or to approve a message: carry on.
- Replies show only the results, precise and short: a table is fine for results (jobs, people, messages sent); no plans, no filler, no explanations unless asked.
