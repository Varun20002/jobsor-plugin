---
name: find-email
description: Find the email address of a person in the JOBSOR tracker, label how sure it is (published, checked, checked (accept-all), guessed), and never claim a guess as found. Use when the user asks "find their email", when a JOBSOR person has no email, or when the JOBSOR round reaches people without an email.
---

# Find the email

Read the profile and the person's row. Work in this order and stop at the first address that is **published** or **checked**.
Write the address and its label in the People tab: `published`, `checked`, `checked (accept-all)`, or `guessed (not checked)`.

1. **An address the person published.** Their hiring post, the company's team page, a talk page, their own site. One Exa search:
   `"<full name>" "<company>" (email OR contact OR "@<domain>")`. An email is theirs only when the part before the @ carries their name
   (both names in full for a personal Gmail-type address). Shared mailboxes (careers@, hr@, jobs@, info@) are never a person's address;
   keep a careers@ address only as the company inbox for a small startup with nobody found. Label: `published`.
2. **The company's domain.** Take it from the job's Notes "Website:" first, then the job link if it is the company's own site, then the
   LinkedIn company page's website, then one search. Not the domain of a job site or a hiring system. Never use a guessed domain (do not
   try name.ai or name.com without a page that shows it).
3. **The company's email format.** Learn it once per company and note it in the job's Notes ("Email format: {first}.{last}@acme.com, from
   2 published addresses"):
   - a page that states the format (search `"@<domain>" email format`), or
   - two published addresses of real people at the domain with the same shape, or
   - Hunter's domain search, if Hunter is connected (it gives the pattern).
   Formats: `{first}.{last}`, `{first}`, `{first}{last}`, `{f}{last}`, `{first}_{last}`, `{first}-{last}`, `{first}{l}`. First and last
   names without titles (Dr, Mr, Ms, Prof, Shri, Smt) and without accents; a double surname is joined ("Rao-Iyer" gives "raoiyer").
4. **Build the address** from the format. With no known format, the common Indian formats in this order: `{first}.{last}`, `{first}`,
   `{first}{last}`, `{f}{last}`, `{first}_{last}`.
5. **Check it (required before any send).** Every built or guessed address is checked. **First, a free mail-server checker** if one is
   connected (a connector with a `verify_email` tool, for example the owner's own JOBSOR email checker; optional): its `status` valid,
   invalid or accept_all is used as below; `unknown` (checker offline, or the company's mail server would not answer) goes on to Hunter.
   Then Hunter's email verifier; **only if Hunter is missing
   or out of credits**, Vibe Prospecting (optional; `enrich-prospects` with contact info for this person, which also returns its own found
   email: label that one `checked` only if Vibe marks it verified). Valid, not accept-all: `checked`. Accept-all or catch-all (also Hunter
   "valid" with accept_all true): `checked (accept-all)`. Unknown: `guessed (not checked)`. Invalid: try the next format (at most 3 checks
   a person). With no checker or no credits: `guessed (not checked)`. A check costs half a Hunter credit, far less than a bounce.

6. **Never stop at "no address found".** If no published or checked address was found, build the best guess from the company's format
   (Hunter's domain search pattern, or two published addresses, or the common formats in order); it is then checked by step 5 and written
   with the label that check gives (`guessed (not checked)` only if it could not be checked). If the person's last name is only an initial
   or missing, use `{first}@domain` first. The person is only left with no address when the company's domain itself is unknown.

## What a label allows
- `published`, `checked` and `checked (accept-all)`: may be sent (if sending is on) or drafted.
- `guessed (not checked)`: **draft only, always** (the old profile line "Send to guessed, unchecked emails" is no longer used).
- A hook refuses a new email to an address that was not checked or read from the tracker as published or checked in this run.
- A bounce later removes the address (the round does this) and the person is tried with the next format or replaced.

## Never
- Never write an address as found when it was built from a format.
- Never use an address from another company's domain for this person.
- Never buy or scrape contact databases, and never copy how a finder's browser extension talks to its servers.

Report per person: the address and its label, or "no address found" (only when the domain is unknown) with what was tried.

## Rules
- **Shared rules:** follow `skills/round/references/shared-rules.md` (read it once per run; a round has already read it).
- **Debug rows:** each person checked writes one row: Step "Find email", Item the person, Tool, Input (address tried), Result (OK / Empty / Hidden /
  Failed), Why (for example "Hunter: no result", "built from {first}.{last}, not checked").
