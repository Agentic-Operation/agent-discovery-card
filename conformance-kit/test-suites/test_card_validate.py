import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VAL = ROOT / "conformance-kit/validators/card_validate.py"
GOOD = ROOT / "examples/loyalty-agent/card.json"


def run(doc):
    tmp = Path("/tmp/_card_case.json")
    tmp.write_text(json.dumps(doc))
    return subprocess.run([sys.executable, str(VAL), str(tmp)], capture_output=True, text=True)


def test_valid_example_passes():
    r = subprocess.run([sys.executable, str(VAL), str(GOOD)], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr


def test_skill_discovery_without_endpoint_fails():
    doc = json.load(open(GOOD))
    for e in doc["extensions"]:
        if "skill-discovery" in e["uri"]:
            del e["params"]["discoveryEndpoint"]
    r = run(doc)
    assert r.returncode == 1 and "discoveryEndpoint" in r.stderr


def test_missing_autonomy_case_at_l3_fails():
    doc = json.load(open(GOOD))
    del doc["autonomyCaseRef"]
    r = run(doc)
    assert r.returncode == 1 and "autonomyCaseRef" in r.stderr


def test_empty_deontics_at_l3_fails():
    doc = json.load(open(GOOD))
    doc["deonticConstraints"] = {"embargoes": [], "burdens": []}
    r = run(doc)
    assert r.returncode == 1 and "deonticConstraints" in r.stderr


def test_cross_env_without_env_instances_fails():
    doc = json.load(open(GOOD))
    doc["extensions"] = [e for e in doc["extensions"] if "environment-instances" not in e["uri"]]
    r = run(doc)
    assert r.returncode == 1 and "environment-instances" in r.stderr


def test_bad_skill_id_fails():
    doc = json.load(open(GOOD))
    doc["skills"][0]["id"] = "TMF-OASF-3015"
    r = run(doc)
    assert r.returncode == 1 and "bad id" in r.stderr


def test_non_https_url_fails():
    doc = json.load(open(GOOD))
    doc["url"] = "http://agents.example.com"
    r = run(doc)
    assert r.returncode == 1
