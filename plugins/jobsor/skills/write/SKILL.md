---
name: write
description: Write the message to a person in the JOBSOR tracker (researched pitch to a founder or hiring manager, recruiter note, peer ask, referral ask, follow-up, thank-you, or a draft reply) from the user's confirmed facts only. Use when the user asks "write to them", "draft a message", "write a follow-up", or when the JOBSOR round has a person ready to contact.
---

# Write the message

Read the profile (confirmed facts, voice, templates, gap and location lines), the job's row, the person's row and earlier messages to
them. Pick the type from the person's Contact as and the history:

| Contact as | First message | Rules |
|---|---|---|
| Hiring manager, Founder | **Researched pitch** (`references/pitch-framework.md`) | Research first; purpose, relevant opening only if found, 2 to 4 proof bullets |
| Recruiter | Recruiter template from the profile | 2 to 4 proof bullets matched to the job's needs; company's job id |
| Peer (to ask) | Peer ask: who is the hiring manager | Peer ask with one line about the user; never a pitch, never a referral ask |
| Referrer (MNC, or a startup peer once the hiring manager is confirmed) | Referral ask template: refer me, or share this with the hiring team | Company job id and link; one line about the user |
| Anyone, no reply after 1 day | Follow-up (`references/followups.md`) | Fixed follow-up template, no AI writing; same thread |
| Peer who named the hiring manager, or a referrer who referred | Thank-you | One or two lines, no new ask |
| A reply from the company | Reply draft for the user | Uses reply facts; never sent by JOBSOR |

## Steps
1. **Facts only.** Pick the confirmed fact lines that fit this job (the must-haves met). Every claim about the user in the message must be
   one of those lines, in its meaning and numbers. Nothing else about the user: no salary, notice period, visa, team size, impact, skill
   or tool that is not a confirmed line. If the user has no work experience, never imply any.
2. **Write** the message for its type. Fill template placeholders only from the job, the person and the facts; drop a line whose
   placeholder has nothing true to fill.
3. **Gap line** when the job asks for more years than the user has (from the profile). **Location line** when the job is in another city;
   for a foreign company hiring remotely, ask whether they would hire remotely from India.
4. **Subject** for email: pitch "{role} at {company} – {user name}"; recruiter or referral "{role} ({company job id}) – {user name}" (drop the
   brackets with no id);
   peer ask "Quick question about the {role} role"; follow-ups keep the thread's subject.
5. **Run every check** in `references/message-checks.md`. Fix and re-check until all pass. If one cannot pass (for example no true opening
   fact was found), keep it as a draft with the reason in Notes, never send it.
6. **Write a Messages row**: type, subject, the opening fact with its date and link, Status "Draft ready". Then hand over to send.

Follow-ups skip steps 1 to 5: fill the fixed template and hand to send.

## Never
- Never invent warmth ("we met", "X suggested", "as discussed", "following our chat") unless the user typed it for this person.
- Never praise ("great post", "inspiring", "loved your talk", "hit home").
- Never cut a message at a character count; write it short from the start.
- Never write JOBSOR's own ids (J001, P002, M003) in any message or subject.
- Never open by telling the person something only about their own job post or company that gives them nothing new.
- Never mention reply facts (CTC, notice period) in a first message.

## Rules
- **Shared rules:** follow `skills/round/references/shared-rules.md` (read it once per run; a round has already read it).
