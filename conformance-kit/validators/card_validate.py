#!/usr/bin/env python3
"""Spec-445 card validator — CI stage 2 (schema + structural rules + extension checks).

Usage: card_validate.py <card.json> [more.json ...]
Exit 0 = conformant; exit 1 = violations on stderr.
"""
import json
import re
import sys
from pathlib import Path

SKILL_ID = re.compile(r"^(TMF-OASF [0-9]+|TMF-GB1033 F-[0-9]+|EXTENSION-[A-Za-z0-9-]+)$")
CID = re.compile(r"^sha256:[a-f0-9]{64}$")
EXT_NS = "https://github.com/tmforum-agents/extensions/"
SKILL_DISCOVERY_URI = EXT_NS + "skill-discovery/v1"


def validate(doc, errors):
    for k in ("id", "name", "description", "version", "uuid", "url", "provider", "classification",
              "capabilities", "authentication", "defaultInputModes", "defaultOutputModes", "skills",
              "impactRadius", "deploymentStatus", "lastUpdated", "spec443_profile_ref"):
        if k not in doc:
            errors.append(f"required field missing: {k}")
    if "content_identifier_cid" in doc and not CID.match(doc["content_identifier_cid"]):
        errors.append("content_identifier_cid must be sha256:<64 hex>")
    for k in ("url",):
        if k in doc and not doc[k].startswith("https://"):
            errors.append(f"{k} must be https")

    c = doc.get("classification", {})
    lvl = c.get("autonomy_level")
    if c.get("agency_class") == "Non-Agentic AI" and lvl in ("L3", "L4", "L5"):
        errors.append("classification: Non-Agentic AI cannot exceed L2")
    if c.get("oda_relationship") != "Standalone" and not doc.get("defaultDataContracts"):
        errors.append("defaultDataContracts required when oda_relationship != Standalone (M-cond)")

    tasks_bound = set()
    for s in doc.get("skills", []):
        if not SKILL_ID.match(s.get("id", "")):
            errors.append(f"skills: bad id {s.get('id')!r} (TMF prefix is part of the ID)")
        tasks_bound.add(s.get("bound_core_task"))

    exts = doc.get("extensions", [])
    uris = [e.get("uri", "") for e in exts]
    for u in uris:
        if not u.startswith(EXT_NS):
            errors.append(f"extensions: uri {u!r} outside TM Forum namespace {EXT_NS}")
    sd = [e for e in exts if e.get("uri") == SKILL_DISCOVERY_URI]
    if sd and sd[0].get("params", {}).get("skillDiscovery") and not sd[0]["params"].get("discoveryEndpoint"):
        errors.append("skillDiscovery: true requires params.discoveryEndpoint")
    if lvl in ("L3", "L4", "L5"):
        if not doc.get("autonomyCaseRef"):
            errors.append("autonomyCaseRef required at L3+")
        dc = doc.get("deonticConstraints", {})
        if not dc.get("embargoes") or not dc.get("burdens"):
            errors.append("deonticConstraints: >=1 embargo and >=1 burden required at L3+")

    ei = [e for e in exts if "environment-instances" in (e.get("uri") or "")]
    if c.get("mobility") != "Static" and not ei:
        errors.append("[EXT] environment-instances extension required when mobility != Static")
    if ei:
        for env in ei[0].get("params", {}).get("environments", []):
            if not env.get("environment") or not env.get("instance_id"):
                errors.append("[EXT] environment-instances entry missing environment/instance_id")

    mg = [e for e in exts if "model-governance" in (e.get("uri") or "")]
    if mg:
        for m in mg[0].get("params", {}).get("models", []):
            if not CID.match(m.get("cid", "")):
                errors.append(f"[EXT] modelGovernance: {m.get('model_id')} bad cid")


def validate_schema(doc, errors):
    try:
        import jsonschema
        schema = json.load(open(Path(__file__).resolve().parents[2] / "schemas" / "agent-card.schema.json"))
        jsonschema.validate(doc, schema)
    except ImportError:
        pass
    except Exception as e:  # noqa: BLE001
        errors.append(f"schema: {e}")


def main():
    paths = sys.argv[1:]
    if not paths:
        print(__doc__)
        return 2
    failed = False
    for p in paths:
        errors = []
        doc = json.load(open(p))
        validate(doc, errors)
        validate_schema(doc, errors)
        if errors:
            failed = True
            for e in errors:
                print(f"{p}: {e}", file=sys.stderr)
        else:
            print(f"{p}: OK")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
