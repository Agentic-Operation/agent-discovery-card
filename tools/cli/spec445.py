#!/usr/bin/env python3
"""spec445 CLI — validate / register / verify / search Spec-445 agent cards.

Subcommands:
  validate <card.json>                 schema + structural lint (card_validate)
  register <card.json> [--registry URL]  validate + POST to registry (default http://localhost:8080)
  verify   <id> [--registry URL]       integrity verification via registry
  search   [--skill-id X] [--autonomy-level L3] [--impact-radius medium] [--registry URL]
  environments <id> [--registry URL]   list per-environment instances
"""
import argparse
import json
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "conformance-kit" / "validators" / "card_validate.py"


def api(method, url, obj=None):
    data = json.dumps(obj).encode() if obj is not None else None
    req = urllib.request.Request(url, data=data, method=method,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name, fn in [("validate", None), ("register", None)]:
        p = sub.add_parser(name)
        p.add_argument("card")
        p.add_argument("--registry", default="http://localhost:8080")
    p = sub.add_parser("verify")
    p.add_argument("id")
    p.add_argument("--registry", default="http://localhost:8080")
    p = sub.add_parser("search")
    p.add_argument("--skill-id")
    p.add_argument("--autonomy-level")
    p.add_argument("--impact-radius")
    p.add_argument("--registry", default="http://localhost:8080")
    p = sub.add_parser("environments")
    p.add_argument("id")
    p.add_argument("--registry", default="http://localhost:8080")
    a = ap.parse_args()

    if a.cmd == "validate":
        r = subprocess.run([sys.executable, str(VALIDATOR), a.card])
        return r.returncode
    if a.cmd == "register":
        r = subprocess.run([sys.executable, str(VALIDATOR), a.card])
        if r.returncode != 0:
            return r.returncode
        code, resp = api("POST", f"{a.registry}/v1/cards", json.load(open(a.card)))
        print(json.dumps(resp))
        return 0 if code == 201 else 1
    if a.cmd == "verify":
        code, resp = api("POST", f"{a.registry}/v1/cards/{a.id}/verify")
        print(json.dumps(resp))
        return 0 if code == 200 and resp.get("verified") else 1
    if a.cmd == "search":
        q = {k: v for k, v in [("skill_id", a.skill_id), ("autonomy_level", a.autonomy_level),
                               ("impactRadius", a.impact_radius)] if v}
        qs = urllib.parse.urlencode(q)
        code, resp = api("GET", f"{a.registry}/v1/cards?{qs}")
        print(json.dumps(resp, indent=2) if code == 200 else resp)
        return 0 if code == 200 else 1
    if a.cmd == "environments":
        code, resp = api("GET", f"{a.registry}/v1/cards/{a.id}/environments")
        print(json.dumps(resp, indent=2))
        return 0 if code == 200 else 1


if __name__ == "__main__":
    sys.exit(main() or 0)
