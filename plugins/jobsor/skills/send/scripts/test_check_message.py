#!/usr/bin/env python3
"""Tests for check_message.py. Run: python3 -I test_check_message.py"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "check_message.py")
FACTS = "Built a billing dashboard at Lumo Labs that cut report time from 14 hours to 3 hours. Handled 200-300 tickets a week."
JOB = "Associate Product Manager at Zesty. Owns the onboarding funnel. 1 to 2 years."
SIG = "\nRegards,\nAsha Rao\nlinkedin.com/in/asharao"
GOOD = ("Hi Ravi,\nI am writing about the Associate Product Manager role at Zesty.\n"
        "At Lumo Labs I built a billing dashboard that cut report time from 14 hours to 3 hours.\n"
        "Can we have a quick chat?" + SIG)


def msg(body, typ="pitch", subject="Associate Product Manager at Zesty", linkedin="https://www.linkedin.com/in/asharao"):
    return {"type": typ, "subject": subject, "body": body, "facts": FACTS, "job_text": JOB,
            "name": "Asha Rao", "linkedin": linkedin, "first_name": "Ravi"}


def run(args, stdin=None):
    r = subprocess.run([sys.executable, "-I", SCRIPT] + args, input=stdin, capture_output=True, text=True)
    return r.returncode, json.loads(r.stdout) if r.stdout.strip() else {}


def check(m):
    path = os.path.join(os.environ.get("TMPDIR", "/tmp"), "jobsor_check_test.json")
    with open(path, "w") as f:
        json.dump(m, f)
    try:
        return run([path])
    finally:
        os.remove(path)


n = 0


def ok(m, expect_pass, needle=None):
    global n
    code, out = check(m)
    assert out["pass"] == expect_pass, (out, m["body"])
    assert code == (0 if expect_pass else 3), code
    if needle:
        assert any(needle in p for p in out["problems"]), out
    n += 1


ok(msg(GOOD), True)
ok(msg(GOOD.replace("Hi Ravi,", "Hi Ravi,\nRe J003.")), False, "J003")
ok(msg(GOOD.replace("Zesty.\n", "Zesty.\nYour post on 12 Nov caught my eye.\n", 1)), False, "12 Nov")
ok(msg(GOOD.replace("Can we", "I cut costs by 45%. Can we")), False, "number 45")
ok(msg(GOOD.replace("I am writing", "Congrats on the launch. I am writing")), False, "congrats")
ok(msg(GOOD.replace("I am writing", 'Your post said "this is amazing work". I am writing')), True)
FU = "Hi Ravi,\nFollowing up on my previous message. Please let me know if this aligns with you." + SIG
ok(msg(FU, "followup"), True)
ok(msg(FU.replace("aligns with you.", "aligns with you. I also attached more."), "followup"), False, "fixed text")
ok(msg(FU + "\n\nOn Mon, 3 Nov 2025 at 10:00, Ravi <r@zesty.com> wrote:\n> Hello Asha\n> Thanks", "followup"), True)
ok(msg("Hi Ravi,\n" + " ".join(["word"] * 120) + SIG, "peer"), False, "too long")
ok(msg(GOOD.replace("linkedin.com/in/asharao", "")), False, "LinkedIn")
ok(msg(GOOD.replace("Can we have a quick chat?", "- a\n- b\n- c\n- d\n- e\nCan we chat?")), False, "5 bullets")
ok(msg(GOOD.replace("quick chat?", "quick chat? Or a call?")), False, "question")
code, out = run(["--hook"], json.dumps({"tool_input": {"to": "r@zesty.com", "subject": "JOBSOR-HOOK-TEST", "body": "Hi Ravi,\nHello."}}))
assert code == 3 and not out["pass"] and "hook test" in out["problems"][0], out
n += 1
code, out = run(["--hook"], json.dumps({"tool_input": {"to": "r@zesty.com", "subject": "Product role", "body": "Hi Ravi,\nA short note."}}))
assert code == 0 and out["pass"], out
n += 1
print(f"ok {n} tests")
