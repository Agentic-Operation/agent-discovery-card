# Quickstart: publish your first Spec-445 card

1. Start from `examples/loyalty-agent/card.json` (Phase 1) — its identity fields join to the Spec-443
   profile and Spec-444 bootstrap of the same agent.
2. Populate required fields: `id`, `name`, `description`, `version`, `uuid`, `url`, `provider`
   (organization/url/contactEmail), `classification`, `capabilities`, `authentication`,
   `defaultInputModes`/`defaultOutputModes`, `skills[]` (with `source_taxonomy`, `bound_core_task`),
   `impactRadius`, `deploymentStatus`, `lastUpdated`, `tmf443_profile_ref` (+ `tmf444_bootstrap_ref`).
3. Conditional fields: `defaultDataContracts` (unless `oda_relationship: Standalone`),
   `autonomyCaseRef` (L3+), `extensions[].uri` + `discoveryEndpoint` (if skillDiscovery).
4. Spec-445 extensions: add `environment-instances` and `modelGovernance` via the A2A `extensions` array
   with TMF-namespaced URIs.
5. Validate: `spec445 validate` against `schemas/agent-card.schema.json` + Annex-C cross-check
   (identity/skills/tools/auth joins vs the sibling artifacts); `pre-commit run --all-files`.
6. Register: `spec445 register` → discoverable at `/.well-known/woa.json`; verify at runtime via the
   stage-3 integrity check.
