# JOBSOR plugin: decisions and why

Newest last. Each line: the decision, the date, the reason. Add to it when the owner decides something; never rewrite old entries
(add a new one that replaces it).

## Scope and way of working
- **Plugin only; the main project is frozen** (21 Nov 2026). Push only `jobsor-plugin`. Reason: the website project must not change.
- **No unasked edits** (17 Nov 2026). Questions get answers; change only what was asked. Reason: extra "helpful" changes were undone.
- **Opus advises, Sonnet executes** (owner, repeated each task in Nov 2026). Opus writes the spec and reviews; Sonnet edits and tests.
- **Product, not personal tool**: built for many users on free plans with their own keys; examples general, never about the owner.

## Rules moved into code (0.2.42 to 0.2.44)
- Counts, windows and scores are kept by scripts and hooks, judgement (reading a job, fit, proof, writing) stays with the AI.
  Reason: in real rounds the AI skipped Apify "to save credits", used level words on Indeed, stopped people search early, and used
  Level scores outside 15/12/8.

## Emails
- **Every guessed address is checked before sending; unchecked guesses stay drafts** (owner, 25 Nov 2026). Reason: 2 of 10 unchecked
  guesses bounced (20%), 0 of 10 checked ones; bounces hurt the user's Gmail. Accept-all results may be sent (one such reply came).
- **Keep the web-search route for people (Exa, Firecrawl) and pattern guessing; do not make Hunter's paid reveal the first step**
  (25 Nov 2026, after a devil's-advocate review). Reason: a reveal costs 1 credit vs 0.5 for checking a guess; Hunter's free preview
  found 1 recruiter at a 532-person company; its data is inferred and still needs proof. Hunter's free preview stays an optional extra.
- **Apollo is out for free users**: its free plan refuses API people search and email lookups (tested 12 Nov and 25 Nov 2026).
- **Owner's own email checker (Reacher on his Mac) is used first, Hunter second** (25-27 Nov 2026). Reason: free and unlimited for
  the owner, 13/13 correct in the test. Not for other users from a home connection (blacklisting risk, privacy, laptop uptime); for
  users later: a rented port-25 server with per-user keys, only after revenue.
- **Up to 5 format checks a person, at most 3 on Hunter** (27 Nov 2026). Reason: the free checker makes extra tries cheap.

## Phones and WhatsApp (discussed 27 Nov 2026, nothing built)
- Never automate Truecaller, GPay or similar lookups (their rules, India's DPDP Act, account bans). The user verifies a number by hand.
- If phone numbers are added: only published ones (hiring posts) and Hunter's free field; paid lookups only on request.
- If WhatsApp is added: `wa.me` ready-to-send links the user taps; not a linked-WhatsApp connector, not Meta's business API.
