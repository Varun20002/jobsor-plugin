---
name: find-email
description: Find the email address of a person in the JOBSOR tracker, label how sure it is (published, checked, guessed), and never claim a guess as found. Use when the user asks "find their email", when a JOBSOR person has no email, or when the JOBSOR round reaches people without an email.
---

# Find the email

Read the profile and the person's row. Work in this order and stop at the first address that is **published** or **checked**.
Write the address and its label in the People tab: `published`, `checked`, or `guessed (not checked)`.

1. **An address the person published.** Their hiring post, the company's team page, a talk page, their own site. One Exa search:
   `"<full name>" "<company>" (email OR contact OR "@<domain>")`. An email is theirs only when the part before the @ carries their name
   (both names in full for a personal Gmail-type address). Shared mailboxes (careers@, hr@, jobs@, info@) are never a person's address;
   keep a careers@ address only as the company inbox for a small startup with nobody found. Label: `published`.
2. **The company's domain.** From the job link when it is the company's own site, else its website from search. Not the domain of a job
   site or a hiring system.
3. **The company's email format.** Learn it once per company and note it in the job's Notes ("Email format: {first}.{last}@acme.com, from
   2 published addresses"):
   - a page that states the format (search `"@<domain>" email format`), or
   - two published addresses of real people at the domain with the same shape, or
   - Hunter's domain search, if Hunter is connected (it gives the pattern).
   Formats: `{first}.{last}`, `{first}`, `{first}{last}`, `{f}{last}`, `{first}_{last}`, `{first}-{last}`, `{first}{l}`. First and last
   names without titles (Dr, Mr, Ms, Prof, Shri, Smt) and without accents; a double surname is joined ("Rao-Iyer" gives "raoiyer").
4. **Build the address** from the format. With no known format, the common Indian formats in this order: `{first}.{last}`, `{first}`,
   `{first}{last}`, `{f}{last}`, `{first}_{last}`.
5. **Check it**, if a checker is connected: Hunter's email verifier, or Bird's email lookup. Valid means `checked`. "Accept all" or
   "catch-all" proves nothing: the address stays `guessed (not checked)`. Invalid: try the next format (at most 3 checks a person). With no
   checker, the address stays `guessed (not checked)`.

## What a label allows
- `published` and `checked`: the send skill may send (if sending is on) or draft.
- `guessed (not checked)`: draft only, unless the profile says "Send to guessed, unchecked emails: yes".
- A bounce later removes the address (the round does this) and the person is tried with the next format or replaced.

## Never
- Never write an address as found when it was built from a format.
- Never use an address from another company's domain for this person.
- Never buy or scrape contact databases, and never copy how a finder's browser extension talks to its servers.

Report per person: the address and its label, or "no address found" with what was tried.

## Autopilot and short replies (every JOBSOR skill)
- Never stop to ask the user to pick a job or a person, or to approve a message. Carry on through the next steps the round would take.
  Ask only when nothing can be done without an answer.
- Every reply to the user is at most 5 short lines. No tables, no lists of what you will do, no explanations unless asked.
