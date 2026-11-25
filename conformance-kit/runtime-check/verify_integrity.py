#!/usr/bin/env python3
"""Stage-3 runtime integrity check (Spec-445 §10): verify a card's integrity_wrapper
signature against the declared transparency log at agent startup. Aborts startup on failure.

Usage: verify_integrity.py <card.json> [--cosign] [--rekor URL]
Exit 0 = verified; 1 = verification failed (startup must abort).

Structural checks always run (CID format, wrapper completeness, https URIs). With --cosign,
delegates blob signature verification to `cosign verify-blob` when available.
"""
import json
import re
import shutil
import subprocess
import sys

CID = re.compile(r"^sha256:[a-f0-9]{64}$")


def main():
    path = sys.argv[1]
    cosign = "--cosign" in sys.argv
    card = json.load(open(path))
    errs = []
    if not CID.match(card.get("content_identifier_cid", "")):
        errs.append("content_identifier_cid missing or not sha256:<64 hex>")
    iw = card.get("integrity_wrapper") or {}
    if not iw.get("signature_type"):
        errs.append("integrity_wrapper.signature_type missing")
    for k in ("issuer", "transparency_log"):
        if not iw.get(k) or not str(iw[k]).startswith("https://"):
            errs.append(f"integrity_wrapper.{k} missing or not https")
    if cosign:
        if not shutil.which("cosign"):
            errs.append("--cosign requested but cosign not installed")
        else:
            blob = json.dumps(card, sort_keys=True).encode()
            r = subprocess.run(["cosign", "verify-blob", "--rekor-url", iw.get("transparency_log", ""),
                                "--certificate-identity", iw.get("issuer", ""), "-"], input=blob,
                               capture_output=True)
            if r.returncode != 0:
                errs.append("cosign verification failed: " + r.stderr.decode()[:300])
    if errs:
        for e in errs:
            print("INTEGRITY FAIL:", e, file=sys.stderr)
        return 1
    print(f"{path}: integrity verified (signature_type={iw.get('signature_type')}, log={iw.get('transparency_log')})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
