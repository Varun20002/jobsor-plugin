#!/usr/bin/env python3
"""Tests for jobsor.py. Run: python3 -I test_jobsor.py"""
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "jobsor.py")
HOME = tempfile.mkdtemp()
TMP = tempfile.mkdtemp()
N = 0


def run(args, stdin=""):
    env = dict(os.environ, HOME=HOME)
    r = subprocess.run([sys.executable, "-I", SCRIPT] + args, input=stdin, capture_output=True, text=True, env=env)
    try:
        data = json.loads(r.stdout) if r.stdout.strip() else None
    except Exception:
        data = None
    return r.returncode, data, r.stderr


def check(cond, msg):
    global N
    assert cond, msg
    N += 1


def plan(now, log="", sources="apify,indeed"):
    return run(["plan", "--now", now, "--log", log, "--sources", sources])


c, d, _ = plan("2026-11-24T10:00")
check(c == 0 and d["window"] == "morning" and {"apify", "indeed", "post-search"} <= set(d["due"]), "morning")
c, d, _ = plan("2026-11-24T10:00", "x window: Morning 2026-11-24 y")
check(not ({"apify", "indeed", "post-search"} & set(d["due"])) and "replies" in d["due"], "ran")
c, d, _ = plan("2026-11-24T16:00")
check(d["window"] == "afternoon" and "apify" not in d["due"] and "indeed" in d["due"], "afternoon")
c, d, _ = plan("2026-11-24T03:00")
check(d["quiet"] is True and d["due"] == [] and c == 0, "quiet")
c, d, _ = plan("2026-11-24T22:00", "", "")
check(d["window"] == "night" and "indeed" not in d["due"], "night no sources")

c, d, _ = run(["score", "--work", "33", "--must", "25", "--user-years", "0.5", "--job-min-years", "1"])
check(c == 0 and d["level"] == 15 and d["match"] == 73, "score 73")
c, d, _ = run(["score", "--work", "33", "--must", "25", "--user-years", "0.5"])
check(d["level"] == 12 and d["match"] == 70, "level 12")
c, d, _ = run(["score", "--work", "40", "--must", "35", "--user-years", "0.5", "--job-min-years", "2.5"])
check(d["level"] == 8 and d["stretch"] and d["match"] == 60, "stretch cap")
c, d, _ = run(["score", "--work", "20", "--must", "20", "--user-years", "0.5", "--job-min-years", "2.5"])
check(d["match"] == 48, "stretch under cap")
c, d, _ = run(["score", "--work", "30", "--must", "30", "--user-years", "1", "--duties-above"])
check(d["level"] == 8 and d["match"] == 60, "duties above")
c, d, _ = run(["score", "--work", "33", "--must", "25", "--user-years", "0", "--job-min-years", "3"])
check(c == 3 and d["hide"] is True, "hide")
c, d, _ = run(["score", "--work", "50", "--must", "25", "--user-years", "0"])
check(c == 2, "range")

c, d, _ = run(["people", "--route", "startup-no-hm", "--found", "4", "--searches", "1", "--empty-in-row", "0"])
check(c == 3 and d["done"] is False and d["next"], "people more")
c, d, _ = run(["people", "--route", "startup-no-hm", "--found", "10", "--searches", "3", "--empty-in-row", "0"])
check(c == 0, "people done")
c, d, _ = run(["people", "--route", "startup-no-hm", "--found", "4", "--searches", "3", "--empty-in-row", "2"])
check(c == 0, "people empty")
c, d, _ = run(["people", "--route", "agency", "--found", "0", "--searches", "8", "--empty-in-row", "0"])
check(c == 0, "people searches cap")

c, _, e = run(["indeed-hook"], json.dumps({"tool_input": {"search": "associate product manager entry level"}}))
check(c == 2 and "plain role words" in e, "hook level")
c, _, _ = run(["indeed-hook"], json.dumps({"tool_input": {"search": "associate product manager"}}))
check(c == 0, "hook plain")
c, _, _ = run(["indeed-hook"], "not json")
check(c == 0, "hook bad json")


def transcript(name, entries):
    p = os.path.join(TMP, name)
    with open(p, "w") as f:
        for e in entries:
            f.write(json.dumps(e) + "\n")
    return p


def use(name, inp=None):
    return {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": name, "input": inp or {}}]}}


ROUND = use("Skill", {"skill": "jobsor:round"})
stop = lambda p, active=False: run(["stop-hook"], json.dumps({"transcript_path": p, "stop_hook_active": active}))
check(stop("/nonexistent", True)[0] == 0, "stop active")
plan("2026-11-24T10:00")  # fresh plan, due: apify, indeed, post-search
check(stop(transcript("a.jsonl", [ROUND]))[0] == 2, "stop missing")
full = [ROUND, use("mcp__plugin_jobsor_apify__call-actor"), use("mcp__plugin_jobsor_indeed__search_jobs"),
        use("mcp__plugin_jobsor_firecrawl__firecrawl_search")]
check(stop(transcript("b.jsonl", full))[0] == 0, "stop all present")
check(stop(transcript("c.jsonl", [use("mcp__x__other")]))[0] == 0, "not a round")
check(stop(transcript("d.jsonl", [{"type": "user", "message": {"content": "/jobsor:round"}}]))[0] == 2, "round by user text")
U = lambda t: {"type": "user", "message": {"content": t}}
check(stop(transcript("f.jsonl", [U("This session is being continued ... mentions /jobsor:round ...")]))[0] == 0, "mention only")
check(stop(transcript("g.jsonl", [U("Run the JOBSOR round (/jobsor:round). Profile: ...")]))[0] == 2, "round by first message")
os.remove(os.path.join(HOME, ".jobsor", "round-plan.json"))
check(stop(transcript("e.jsonl", [ROUND]))[0] == 2, "no plan")
print("ok %d tests" % N)
