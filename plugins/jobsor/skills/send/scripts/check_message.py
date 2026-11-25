#!/usr/bin/env python3
"""JOBSOR message check. Plain Python 3, nothing to install, no network, no files written.

Usage: python3 -I check_message.py message.json   (skill mode: every check)
       python3 -I check_message.py --hook          (hook mode: reads a Gmail tool call's JSON on stdin; only the checks that need no facts)
Hook mode also refuses a new email (not a reply) to an address that was not checked in this transcript or read as labelled.
Prints {"pass": true|false, "problems": ["..."]}. Exit 0 = pass, 3 = fail, 2 = bad input.

message.json: type (pitch | recruiter | peer | referral | followup | thankyou | reply), subject, body,
facts (confirmed facts and resume source), job_text (job row, description, the person's post if used),
name (the user's name), linkedin (may be empty), first_name (the recipient's first name).
The quoted earlier thread (from the line "On ... wrote:", and lines starting with ">") is dropped before checking.
"""
import json
import re
import sys

BANNED = [
    "great", "amazing", "inspiring", "impressive", "loved", "fascinating", "brilliant", "kudos", "congrats", "congratulations",
    "hit home", "resonated",
    "passionate", "just checking in", "just following up", "touching base", "circling back", "express my interest", "dear hiring",
    "excited about the opportunity", "thrilled at the prospect", "results-driven", "spearheaded", "leveraged", "delve",
    "hope this email finds you well", "hope this message finds you well", "in today's fast-paced world",
    "we met", "we spoke", "as discussed", "following our chat", "suggested i reach out", "referred me", "great to connect again",
]
MAX_WORDS = {"pitch": 200, "recruiter": 200, "peer": 90, "referral": 90, "thankyou": 60}
FOLLOWUP = "Following up on my previous message. Please let me know if this aligns with you."
MONTHS = r"(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|june?|july?|aug(?:ust)?|sep(?:t(?:ember)?)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)"
DATE_RES = [
    r"\b\d{1,2}(?:st|nd|rd|th)?\s+" + MONTHS + r"\b(?:,?\s+\d{4})?",
    r"\b" + MONTHS + r"\s+\d{1,2}(?:st|nd|rd|th)?\b(?:,?\s+\d{4})?",
    r"\b\d{4}-\d{2}-\d{2}\b",
    r"\b\d{1,2}/\d{1,2}(?:/\d{2,4})?\b",
    r"\bon\s+(?:mon|tues?|wed(?:nes)?|thu(?:rs)?|fri|sat(?:ur)?|sun)(?:day)?\b",
]
CLOSINGS = ("regards", "warm regards", "best regards", "thanks", "thank you", "best", "sincerely", "cheers", "with thanks")


def drop_quote(body):
    out = []
    for line in body.splitlines():
        s = line.strip()
        if re.match(r"^On .*wrote:\s*$", s) or (s.startswith("On ") and s.endswith("wrote:")):
            break
        if s.startswith(">"):
            continue
        out.append(line)
    return "\n".join(out)


def strip_quotes(text):
    return re.sub(r"\"[^\"\n]*\"|“[^”\n]*”", " ", text)


def lines_of(text):
    return [re.sub(r"\s+", " ", l).strip() for l in text.splitlines() if l.strip()]


def norm_link(s):
    return re.sub(r"^https?://", "", s.strip().lower()).replace("www.", "").rstrip("/")


def numbers_in(text):
    text = re.sub(r"(?<=\d),(?=\d)", "", text)
    return set(re.findall(r"\d+(?:\.\d+)?", text))


def split_signature(lines, name):
    """Return (content lines, signature lines): the signature starts at the closing word or the name within the last 6 lines."""
    start = None
    for i in range(max(0, len(lines) - 6), len(lines)):
        low = lines[i].lower().rstrip(",!. ")
        if low in CLOSINGS:
            start = i
            break
    if start is None:
        for i in range(max(0, len(lines) - 6), len(lines)):
            if name and name.lower() in lines[i].lower():
                start = i
                break
    if start is None:
        return lines, []
    return lines[:start], lines[start:]


def common_checks(subject, body, problems):
    both = subject + "\n" + body
    for m in sorted(set(re.findall(r"\b[JPM]\d{3}\b", both))):
        problems.append(f"JOBSOR id {m} in the message")
    if re.search(r"\{[^{}]*\}|\bTODO\b|\bXX+\b", both) or re.search(r"\[\s*your [^\]]*\]", both, re.I):
        problems.append("unfilled placeholder in the message")
    elif any("@" not in t and "://" not in t for t in re.findall(r"<[^<>\n]+>", both)):
        problems.append("unfilled placeholder in the message")
    plain = strip_quotes(both).lower()
    for phrase in BANNED:
        if re.search(r"(?<![\w'-])" + re.escape(phrase) + r"(?![\w-])", plain):
            problems.append(f"banned phrase: {phrase}")
    if "JOBSOR-HOOK-TEST" in subject:
        problems.append("hook test: send refused by the JOBSOR check")


def full_checks(m, subject, body, problems):
    typ = m.get("type", "")
    name = m.get("name", "").strip()
    linkedin = m.get("linkedin", "").strip()
    first = m.get("first_name", "").strip()
    lines = lines_of(body)
    content, sig = split_signature(lines, name)
    if typ == "followup":
        norm = [re.sub(r"\s+", " ", l.strip()) for l in lines]
        ok = len(norm) >= 2 and norm[0].lower() == f"hi {first},".lower() and norm[1] == FOLLOWUP
        if ok:
            for l in norm[2:]:
                low = l.lower().rstrip(",")
                if not (low == "regards" or (name and low == name.lower()) or re.fullmatch(r"[+\d][\d\s()-]{6,}", l)
                        or (linkedin and norm_link(l) == norm_link(linkedin))):
                    ok = False
        if not ok:
            problems.append("follow-up must be the fixed text")
    # 6 date in the opening
    rest = content[1:] if content and re.match(r"(hi|hello|hey|dear)\b", content[0], re.I) else content
    for l in rest[:3]:
        for rx in DATE_RES:
            mm = re.search(rx, l, re.I)
            if mm:
                problems.append(f"date in the opening: {mm.group(0)}")
                break
    # 7 signature
    last = " ".join(lines[-6:])
    if name and name.lower() not in last.lower():
        problems.append("signature is missing the name")
    if linkedin and norm_link(linkedin) not in norm_link(last):
        problems.append("signature is missing the LinkedIn link")
    # 8 length
    words = len(" ".join(content).split())
    if typ in MAX_WORDS and words > MAX_WORDS[typ]:
        problems.append(f"too long: {words} words, at most {MAX_WORDS[typ]}")
    # 9 one ask
    if strip_quotes("\n".join(content)).count("?") > 1:
        problems.append("more than one question mark: one ask only")
    # 10 bullets
    bullets = [l for l in content if re.match(r"^(?:[-*•]|\d+[.)])\s", l)]
    if len(bullets) > 4:
        problems.append(f"{len(bullets)} bullets, at most 4")
    # 11 numbers
    text = "\n".join(re.sub(r"^(?:[-*•]|\d+[.)])\s+", "", l) for l in content)
    text = re.sub(r"https?://\S+|www\.\S+|\S+@\S+\.\S+|\b[JPM]\d{3}\b", " ", text)
    known = numbers_in(m.get("facts", "") + "\n" + m.get("job_text", ""))
    for n in sorted(numbers_in(text), key=lambda x: float(x)):
        if n not in known:
            problems.append(f"number {n} not in the facts or the job")


def walk(obj, found):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, str):
                found.setdefault(k.lower(), []).append(v)
            else:
                walk(v, found)
    elif isinstance(obj, list):
        for v in obj:
            walk(v, found)


def hook_parts(data):
    found = {}
    walk(data, found)
    subject = (found.get("subject") or [""])[0]
    body = ""
    for k in ("body", "message", "text", "content", "htmlbody", "html_body", "plaintextbody", "plain_text_body"):
        if found.get(k):
            body = found[k][0]
            break
    if "<" in body and re.search(r"</?(p|div|br|html|body)\b", body, re.I):
        body = re.sub(r"<br\s*/?>|</p>|</div>", "\n", body, flags=re.I)
        body = re.sub(r"<[^>]+>", "", body)
    return subject, body


def recipients_of(ti):
    out = []
    for k in ("to", "recipient", "recipients"):
        v = ti.get(k)
        vals = v if isinstance(v, list) else [v]
        for x in vals:
            if isinstance(x, str):
                for part in x.split(","):
                    part = part.strip().lower()
                    mm = re.search(r"<([^<>]+)>", part)
                    part = mm.group(1).strip() if mm else part
                    if part:
                        out.append(part)
    return out


def tool_blocks(node, uses, results):
    if isinstance(node, dict):
        t = node.get("type")
        if t == "tool_use":
            uses.append(node)
        elif t == "tool_result":
            results.append(node)
        for v in node.values():
            tool_blocks(v, uses, results)
    elif isinstance(node, list):
        for v in node:
            tool_blocks(v, uses, results)


def all_strings(node, out):
    if isinstance(node, str):
        out.append(node)
    elif isinstance(node, dict):
        for v in node.values():
            all_strings(v, out)
    elif isinstance(node, list):
        for v in node:
            all_strings(v, out)


def unchecked_addresses(data, subject, addrs):
    """Addresses with no check in this transcript. Any failure to read the transcript means no problem (fail open)."""
    try:
        name = str(data.get("tool_name", "")).lower()
        if not (name.endswith("send_message") or name.endswith("send_email")):
            return []
        if subject.strip().lower().startswith("re:") or not addrs:
            return []
        path = data.get("transcript_path")
        if not path:
            return []
        with open(path, encoding="utf-8") as f:
            raw = f.read()
        uses, results = [], []
        for line in raw.splitlines():
            line = line.strip()
            if line:
                try:
                    tool_blocks(json.loads(line), uses, results)
                except ValueError:
                    pass
        result_text = {}
        for r in results:
            strs = []
            all_strings(r.get("content"), strs)
            result_text.setdefault(r.get("tool_use_id"), []).append("\n".join(strs))
        bad = []
        for addr in addrs:
            good = False
            for u in uses:
                if "verif" not in str(u.get("name", "")).lower():
                    continue
                strs = []
                all_strings(u.get("input"), strs)
                if not any(s.strip().lower() == addr for s in strs):
                    continue
                for txt in result_text.get(u.get("id"), []):
                    # The status value, not field names: a Hunter result always has an "accept_all" key, even when invalid.
                    if re.search(r"status\W{0,6}(valid|accept[_ -]?all|catch[_ -]?all)\b|accept[_ -]?all\W{0,6}true", txt, re.I):
                        good = True
            if not good and re.search(r'\\*"' + re.escape(addr) + r'\\*"\s*,\s*\\*"(published|checked|checked \(accept-all\))\\*"', raw, re.I):
                good = True
            if not good:
                bad.append(addr)
        return bad
    except Exception:
        return []


def main():
    args = sys.argv[1:]
    try:
        if args == ["--hook"]:
            data = json.loads(sys.stdin.read() or "{}")
            subject, body = hook_parts(data)
            m = None
            try:
                addrs = recipients_of(data.get("tool_input") or {})
            except Exception:
                addrs = []
        elif len(args) == 1:
            with open(args[0], encoding="utf-8") as f:
                m = json.load(f)
            subject, body = str(m.get("subject", "")), str(m.get("body", ""))
        else:
            raise ValueError("usage")
    except (OSError, ValueError):
        print("usage: check_message.py message.json | --hook", file=sys.stderr)
        return 2
    body = drop_quote(body)
    problems = []
    common_checks(subject, body, problems)
    if m is None:
        for a in unchecked_addresses(data, subject, addrs):
            problems.append(f"address {a} was not checked: run the email checker on it first (find-email step 5) or leave a draft")
    if m is not None:
        full_checks(m, subject, body, problems)
    print(json.dumps({"pass": not problems, "problems": problems}, ensure_ascii=False))
    return 0 if not problems else 3


if __name__ == "__main__":
    sys.exit(main())
