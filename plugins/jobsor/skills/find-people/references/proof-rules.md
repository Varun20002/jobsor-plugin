# Proof in, contradiction out

Ported word for word in meaning from the JOBSOR website (`docs/PEOPLE_PROOF_PLAN.md`, `lib/people-proof.ts`, MASTER decision 47).
Owner: "have proper guardrails, evals, I don't want any fuck ups."

A person is listed only if **(a)** at least one proof says they work at this company now, and **(b)** no contradiction says otherwise.
Anything unsure is left out.

## Proof (any one is enough)
| Proof | Write in the Proof column |
|---|---|
| LinkedIn's "Meet the hiring team" box for this job (a screenshot the user pasted) | "On the hiring team for this job" |
| Their own hiring post for this company, last 30 days (found in the post, or by the reverse search on the job link) | "Posted about this job on 10 Nov" |
| Their own headline names this company as the employer ("Engineer at Acme", "@ Acme", "Design, Acme") | "Headline: Engineering Manager at Acme" |
| Their profile lists a current job at this company ("(Current)", "– Present") | "Current job on profile: PM, Acme" |
| The company's own team or about page names them | "On acme.com/team" |
| A data-provider record (Hunter) **and** a public line that agrees (headline or current job) | "Hunter, confirmed by their profile" |
| A reply from someone at the company naming them as the hiring manager | "Named by P004 in a reply" |

A Hunter record alone is **not** proof (old records). A LinkedIn connections export is proof only if it is under 90 days old.

## Contradictions (any one removes the person)
1. Their own headline (the words before the first "·" or "|") names **another employer**: "Data Scientist at Arctic Wolf".
2. The company is named only as a **past** one: "Ex-Acme", "formerly at Acme", "Acme (2021 – 2024)", "previously Acme".
3. Their profile's **current job is at another company**, and nothing current names this one.
4. They are **outside India** for an India job.
5. A **namesake company**: "Acme Labs" is not "Acme"; check the company's website or LinkedIn page when names are close. ("Acme India" is
   the same company.)
6. Their **work email is at another company's domain**.
7. A post or news says they **left** or joined another company.

Exception: the hiring team box and their own hiring post for this job outrank contradictions 1 and 3 (an agency recruiter can hire for the
company).

## Traps seen in real data (each was a real miss)
- **Search titles like "Name - Headline - Company | LinkedIn":** the company after the headline is the one LinkedIn shows on their
  profile, and it can be an **older** job. It counts as proof only when the headline itself names no other employer and nothing else
  (an "Experience: <other company>" line) says they work elsewhere. "Name - PM at Arctic Wolf - Lumenci": not listed.
  "Name - Sales Manager - Lumenci" with "Experience: Lumenci": listed.
- **"Experience: <company>" in a snippet** is their current employer as LinkedIn shows it: "Experience: Zentrix" for a Lumenci job means
  they work elsewhere (not listed). "Education: Lumenci Academy" is a school, not the company.
- **Hunter or Apollo record with an email at another domain** ("omar@lumenci.io" when the company is lumenci.com): not listed, even if
  confirmed elsewhere.
- **Merging by name:** two records with the same name are one person only when they share the same LinkedIn profile link (or the same
  work email at the company's domain). Two "Rahul Verma"s with different profiles are two people.
- **Surname equals the company:** "Steffy Kulfi" does not work at Kulfi because of her name.
- **"at scale", "at speed"** in a headline are not employers.
- **"Building in Stealth"** headline with a current "Managing Director" job at the company on the profile: listed (as their real title).
  Contact as "Founder" only when a source says they founded the company; a Managing Director or CEO without that is "Hiring manager"
  (company leader), and the message uses their real title.
- **A peer is not the hiring manager** (same title as the job, or "Senior <same title>"): list them as Peer (to ask) or Referrer. The
  hiring manager is a lead, group or principal, head, director, VP or founder in the same function ("Engineering Manager" or "Head of
  Engineering" for a "Backend Engineer" job).
- **A founder found on the company's own team page** ("Co-founder & CEO" on lumenci.com/about) is listed as Founder.
- **The user's own LinkedIn connection** from an export under 90 days old is listed (as Referrer at an MNC); older needs another proof.
- **Abroad:** "Location: London" for an India job: not listed.
