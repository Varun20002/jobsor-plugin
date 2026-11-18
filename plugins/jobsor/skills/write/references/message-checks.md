# Checks before any message is kept

Every message passes all of these. Ported from the JOBSOR website (`lib/compose.ts`, `lib/ai-draft.ts`, owner's rules).

1. **Facts:** re-read the message line by line against the profile's confirmed facts. Every claim about the user (a role, company, date,
   number, skill, tool, result, degree, link) is in a confirmed line with the same meaning and the same numbers. Remove anything that is
   not. Experience in years only as the profile states it.
   **No summary sentences about the user's work.** Never sum up what kind of work they do ("getting people through the first step of a
   flow is the work I've done", "sign-up is the part I can speak to", "this is exactly my area"): put the fact itself and let it speak.
   Linking words count too: "the problem I worked on most recently", "for years", "always", "many times" are claims; use them only if a
   fact says so.
   **Names:** the user's name, sign-off and contact details come only from the profile. With no profile, write "[your name]"; never take
   a name from anywhere else (the computer, an email address, earlier chats).
   **Their side:** say about the person or company only what a source says (their post's words, the news item). No guesses about their
   product, users or problems ("this adds a step where users drop off").
   **No new promises** about what the user would do in the job ("I'd like to improve your funnels as your analyst").
2. **No fake warmth:** none of "we met", "we spoke", "as discussed", "following our chat", "X suggested I reach out", "X referred me",
   "great to connect again", unless the user typed it for this person.
3. **No praise:** none of "great", "amazing", "inspiring", "impressive", "loved", "fascinating", "hit home", "resonated", "brilliant",
   "kudos", "congrats" about the person's work.
4. **No stock phrases** (the website's banned list): passionate, just checking in, just following up, touching base, circling back,
   express my interest, dear hiring, excited about the opportunity, thrilled at the prospect, results-driven, spearheaded, leveraged,
   delve, hope this email finds you well, hope this message finds you well.
5. **Length:** a pitch under about 150 words; a peer ask under about 60 words; a follow-up under about 80 words. Written short, never cut.
6. **One ask:** exactly one question asking for something. A follow-up repeats the first message's ask; if it is not known, the default
   "If this aligns with you, can we have a quick chat?". Never invent a new ask (a "15-minute call this week").
6b. **One story:** a pitch or follow-up tells one confirmed fact as its story; other facts (degree, older work) stay in the resume.
7. **The opening is real:** for a pitch, the opening names a real item with a date and a link the user can open (in the Messages row);
   no made-up names or numbers in it.
8. **Reads as a person wrote it:** plain sentences, no headings, no bullet walls (at most 3 bullets in a recruiter note), no emoji, no
   "In today's fast-paced world".
9. **Right person, right type:** a peer gets only the peer ask; a recruiter is not pitched as if they were the hiring manager; an MNC
   person is never asked "who is the hiring manager".
10. **Names:** the person's first name is spelled as in their own profile or post.
