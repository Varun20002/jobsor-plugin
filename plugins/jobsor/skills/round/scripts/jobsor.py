#!/usr/bin/env python3
"""JOBSOR round rules kept by code. Plain Python 3, nothing to install, no network.

Usage: python3 -I jobsor.py plan --log "<last 3 Log rows>" --sources apify,indeed [--now YYYY-MM-DDTHH:MM]
       python3 -I jobsor.py score --work W --must M --user-years U [--job-min-years Y] [--duties-above]
       python3 -I jobsor.py people --route startup-hm|startup-no-hm|mnc|agency --found N --searches S --empty-in-row E
       python3 -I jobsor.py indeed-hook   (PreToolUse hook: reads a tool call's JSON on stdin)
       python3 -I jobsor.py stop-hook     (Stop hook: reads the Stop JSON on stdin)
Prints one JSON object on stdout. Exit 0 = ok/done, 3 = not ok (act on "problems" / "next"), 2 = bad input (hooks: 2 = block).
All times are India time (UTC + 5:30, fixed offset). --now overrides the clock, for tests.
"""
import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone

IST = timezone(timedelta(hours=5, minutes=30))
PLAN_FILE = os.path.join("~", ".jobsor", "round-plan.json")
LEVEL_WORDS = ["entry level", "entry-level", "fresher", "freshers", "0-1 year", "0 to 1 year", "graduate trainee"]
TARGETS = {"startup-hm": 4, "startup-no-hm": 10, "mnc": 13, "agency": 1}
NEXT = [
    "search other titles in the same function",
    "search a more senior title in the same function (lead, head, manager, director)",
    "search a junior title in the same function (associate, analyst)",
    "search in a second city, or 'India'",
    "read the company's team page",
    "run a Hunter domain search for the function",
]


def out(obj, code=0):
    print(json.dumps(obj, ensure_ascii=False))
    sys.exit(code)


def bad(msg):
    out({"error": msg}, 2)


def now_ist(arg):
    if not arg:
        return datetime.now(timezone.utc).astimezone(IST)
    try:
        return datetime.strptime(arg, "%Y-%m-%dT%H:%M").replace(tzinfo=IST)
    except ValueError:
        bad("--now must look like 2026-11-24T10:00")


def plan_file():
    return os.path.expanduser(PLAN_FILE)


def cmd_plan(a):
    now = now_ist(a.now)
    sources = {s.strip().lower() for s in (a.sources or "").split(",") if s.strip()}
    date = now.strftime("%Y-%m-%d")
    h = now.hour
    if h < 9:
        res = {"quiet": True, "due": []}
    else:
        window = "morning" if h < 15 else "afternoon" if h < 21 else "night"
        marker = "window: %s %s" % (window, date)
        ran = marker in (a.log or "").lower()
        due = ["replies", "follow-ups", "alerts"]
        if not ran:
            due.append("post-search")
            if "indeed" in sources:
                due.append("indeed")
            if window == "morning":
                if "apify" in sources:
                    due.append("apify")
                due.append("cant-read-retry")
        res = {"quiet": False, "window": window, "date": date, "due": due, "log_marker": marker}
    saved = dict(res, made_at=datetime.now(timezone.utc).astimezone(IST).isoformat(timespec="seconds"))
    try:
        p = plan_file()
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w") as f:
            json.dump(saved, f)
    except Exception:
        pass
    out(res)


def cmd_score(a):
    if not 0 <= a.work <= 45:
        bad("--work must be 0 to 45")
    if not 0 <= a.must <= 40:
        bad("--must must be 0 to 40")
    y, u = a.job_min_years, a.user_years
    if y is not None and y > u + 2:
        out({"hide": True, "why": "asks more than the user's years + 2"}, 3)
    stretch = a.duties_above or (y is not None and y >= u + 2)
    if stretch:
        level = 8
    elif y is None:
        level = 12
    else:
        level = 15
    match = int(a.work + a.must + level + 0.5)
    if stretch:
        match = min(match, 60)
    out({"work": a.work, "must": a.must, "level": level, "stretch": bool(stretch), "match": match,
         "notes": "Work %g/45, Must %g/40, Level %d/15 = %d" % (a.work, a.must, level, match)})


def cmd_people(a):
    t = TARGETS[a.route]
    if a.found >= t or a.empty_in_row >= 2 or a.searches >= 8:
        out({"done": True, "target": t, "found": a.found})
    out({"done": False, "target": t, "found": a.found, "next": NEXT[a.searches % len(NEXT)]}, 3)


def read_stdin_json():
    try:
        return json.loads(sys.stdin.read())
    except Exception:
        return None


def cmd_indeed_hook(a):
    d = read_stdin_json()
    try:
        text = str(d["tool_input"]["search"]).lower()
    except Exception:
        sys.exit(0)
    if any(w in text for w in LEVEL_WORDS):
        sys.stderr.write("JOBSOR: search Indeed with plain role words only (for example 'associate product manager'); "
                         "level words make Indeed return unrelated jobs. Seniority is filtered later by job-rules.\n")
        sys.exit(2)
    sys.exit(0)


def parse_time(s):
    try:
        return datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    except Exception:
        return None


def walk(o):
    if isinstance(o, dict):
        yield o
        for v in o.values():
            yield from walk(v)
    elif isinstance(o, list):
        for v in o:
            yield from walk(v)


def cmd_stop_hook(a):
    try:
        d = read_stdin_json() or {}
        if d.get("stop_hook_active"):
            sys.exit(0)
        entries = []
        with open(d["transcript_path"]) as f:
            for line in f:
                try:
                    entries.append(json.loads(line))
                except Exception:
                    pass
        # A round: the round skill was run (Skill tool or the /jobsor:round command), or the session's first typed message STARTS
        # with "run the jobsor round" or "/jobsor:round" (the scheduled task's prompt). A first message that merely mentions the
        # round, mentions inside files, tool results or later chat do not count.
        is_round = False
        calls = []  # (name, time)
        first_user = True
        for e in entries:
            if not isinstance(e, dict):
                continue
            t = parse_time(e.get("timestamp"))
            for n in walk(e):
                if n.get("type") == "tool_use":
                    name = str(n.get("name", ""))
                    calls.append((name.lower(), t))
                    sk = str((n.get("input") or {}).get("skill", "")).lower() if isinstance(n.get("input"), dict) else ""
                    if name == "Skill" and "jobsor" in sk and sk.endswith("round"):
                        is_round = True
            msg = e.get("message") if isinstance(e.get("message"), dict) else {}
            if e.get("type") == "user" and msg.get("role", "user") == "user":
                c = msg.get("content")
                texts = [c] if isinstance(c, str) else [b.get("text", "") for b in c or [] if isinstance(b, dict)
                                                         and b.get("type") == "text"]
                if not texts:
                    continue  # a tool result, not a typed message
                low = " ".join(str(x) for x in texts).lower()
                if "<command-name>/jobsor:round" in low or (
                        first_user and low.lstrip().startswith(("run the jobsor round", "/jobsor:round"))):
                    is_round = True
                first_user = False
        if not is_round:
            sys.exit(0)
        try:
            with open(plan_file()) as f:
                plan = json.load(f)
            made = parse_time(plan.get("made_at"))
            if made is None or datetime.now(timezone.utc) - made > timedelta(hours=3):
                raise ValueError("old")
        except Exception:
            sys.stderr.write("JOBSOR round: run the plan step first (skills/round/scripts/jobsor.py plan) and do what it lists "
                             "before ending.\n")
            sys.exit(2)
        if plan.get("quiet"):
            sys.exit(0)
        later = [n for n, t in calls if t is None or t >= made]
        checks = {"apify": lambda n: "apify" in n and "call-actor" in n, "indeed": lambda n: n.endswith("search_jobs"),
                  "post-search": lambda n: "firecrawl" in n}
        missing = [i for i in plan.get("due", []) if i in checks and not any(checks[i](n) for n in later)]
        if missing:
            sys.stderr.write("JOBSOR round not finished: %s due this window but not run. Run them now (find-jobs sources 3, 5, 6). "
                             "If a connector is not connected or failed, write that in the Log row and the debug log, then end.\n"
                             % ", ".join(missing))
            sys.exit(2)
    except SystemExit:
        raise
    except Exception:
        pass
    sys.exit(0)


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd")
    s = sub.add_parser("plan")
    s.add_argument("--log", default="")
    s.add_argument("--sources", default="")
    s.add_argument("--now")
    s = sub.add_parser("score")
    s.add_argument("--work", type=float, required=True)
    s.add_argument("--must", type=float, required=True)
    s.add_argument("--user-years", type=float, required=True)
    s.add_argument("--job-min-years", type=float)
    s.add_argument("--duties-above", action="store_true")
    s = sub.add_parser("people")
    s.add_argument("--route", choices=sorted(TARGETS), required=True)
    s.add_argument("--found", type=int, required=True)
    s.add_argument("--searches", type=int, required=True)
    s.add_argument("--empty-in-row", type=int, required=True)
    sub.add_parser("indeed-hook")
    sub.add_parser("stop-hook")
    try:
        a = p.parse_args()
    except SystemExit:
        sys.exit(2)
    fn = {"plan": cmd_plan, "score": cmd_score, "people": cmd_people, "indeed-hook": cmd_indeed_hook, "stop-hook": cmd_stop_hook}.get(a.cmd)
    if not fn:
        bad("unknown command")
    fn(a)


if __name__ == "__main__":
    main()
