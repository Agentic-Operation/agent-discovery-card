# Agent Card Registry (reference implementation)

Implements `api/openapi/registry-api.yaml` (Spec-445): card registration with validation, search
(by skill id / taxonomy / autonomy / impact radius / status), versioned retrieval, integrity
verification, per-environment instance registration (`environment-instances` extension, called by
the Spec-444 rollout controller), and WoA discovery at `/.well-known/woa.json`.

Run: `python integrations/registry/registry.py --port 8080 --store cards.json`
CLI: `python tools/cli/spec445.py validate|register|verify|search|environments ...`

Stage-3 runtime check: `conformance-kit/runtime-check/verify_integrity.py <card.json> [--cosign]`
