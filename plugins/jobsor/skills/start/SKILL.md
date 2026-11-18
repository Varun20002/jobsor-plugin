---
name: start
description: Start or check JOBSOR, the job-search plugin for India. Use when the user types /jobsor:start, says "start JOBSOR", asks what JOBSOR does or how to set it up, or asks whether their JOBSOR connectors are working.
---

# Start JOBSOR

JOBSOR helps a job seeker in India reach a real person for each job: it finds fresh jobs, finds the hiring manager, founder, recruiter or
referrer with proof they work at the company now, finds their email, writes a short researched message from facts the user confirmed,
sends it from the user's Gmail or leaves a draft, tracks everything, and follows up until someone at the company replies.

## What to do

1. **Say what JOBSOR does** in one short line: "JOBSOR finds jobs, finds the right person, writes and sends for you, every hour."

2. **Check the three connectors**, one harmless read each. Do not send, draft, or change anything.
   - **Gmail:** search the user's mail for one message from the last day (any message). Report only "works" or the error. Do not show
     the message.
   - **Exa:** one web search for `hiring product manager Bengaluru`. Report "works" or the error.
   - **Firecrawl:** one search for `careers page Razorpay`. Report "works" or the error.
   Gmail is **Claude's own Gmail connector**, not one inside the plugin (Google's sign-in only works with the connector Claude itself
   registered with Google). If Gmail is missing, tell the user: on claude.ai open **Settings, then Connectors**, find **Gmail**, click
   Connect and sign in with Google; in Claude Code the same connector appears once they are signed in with that Claude account. If Exa or
   Firecrawl is missing, tell the user to add it on the plugin's **Connectors** tab (Customize, then Plugins, then JOBSOR, then
   Connectors), then sign in.
   If two Gmail connectors answer, use the one that works and ignore the other.

3. **Report in one line** if all work ("Gmail, Exa and Firecrawl work."); otherwise one line per broken one with the fix. No table.

4. **Next step:** when all three work and there is no profile, go straight into the setup skill: "Attach your resume PDF and I'll set
   everything up."  If a JOBSOR profile already exists and its "Plugin version:" is older than this plugin's version (or missing), say "JOBSOR was
   updated; type `/jobsor:update` to add what's new (a minute or two)." Otherwise, if a profile exists, run a round now (`/jobsor:round`) without asking.

## What JOBSOR can do (for "what can you do")
- `/jobsor:update`: after JOBSOR is updated, runs only what is new for you.
- `/jobsor:setup`: your profile (confirmed facts, roles, cities, sending) and tracker, and the hourly round.
- `/jobsor:round`: replies and bounces, follow-ups, new jobs three times a day, people, messages, a report.
- `/jobsor:find-jobs`: jobs from links you paste, your job-alert emails, hiring posts and companies you name.
- `/jobsor:find-people`: the hiring manager, founder, recruiter or referrer for a job, each with proof they work there now.
- `/jobsor:resume`: a one-page resume tailored to one job, from your own resume lines only; the round makes one for every job it writes for.
- `/jobsor:write` and `/jobsor:send`: a short message from your confirmed facts, as a Gmail draft or sent for you, with that job's resume.
- Optional connectors that help: Apify (LinkedIn jobs, about $0.15 a day on your own Apify account), Hunter (find and check emails), Indeed
  (more jobs), Google Calendar (interviews).

## Rules (every JOBSOR skill keeps these)

- Write only what the user confirmed about themselves. Never invent a fact, a number, a skill, a company or a warm connection.
- Never log in to LinkedIn and never message anyone on LinkedIn for the user.
- Never send an email unless the user turned sending on; otherwise leave a draft.
- Never copy the text of the user's mail into any file; keep only links, titles, companies, names and dates.
- Never try to get past a "not a robot" check on any website; skip that page.
- Plain, short words. Never stop to ask the user to pick a job or a person or to approve a message: carry on.
- Replies show only the results, precise and short: a table is fine for results (jobs, people, messages sent); no plans, no filler, no explanations unless asked.
