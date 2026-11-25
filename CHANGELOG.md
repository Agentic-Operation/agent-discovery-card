# Changelog

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versions follow SemVer.

## [Unreleased]

### Added

- Phase 0 communication package: triad overview, audience one-pagers, model management authority
  overview, glossary, FAQ, conformance cheat sheet, worked-example walkthrough, references index,
  architecture diagrams (mermaid).
- Repo scaffolding: `docs/`, `spec/`, `schemas/`, `examples/`, `conformance-kit/`, `api/`, `tools/`,
  `integrations/`, `user-tools/`, `tests/`, GitHub templates and docs-lint workflow, pre-commit config.

### Added (Phase 1)

- `spec/SPEC-445.md` normative draft v1.0.0-alpha (additive over A2A v1.0) with [EXT]:
  canonical skillDiscovery URI, `coordination.topology_ref`, `environment-instances` extension (E1),
  `modelGovernance` extension (E2); annexes: delta-vs-TMF445, cross-check-manifest, self-check.
- `schemas/agent-card.schema.json` (normative); worked example `examples/loyalty-agent/card.json`
  incl. environment instances + model governance.
- `conformance-kit/`: `card_validate.py`, `crosscheck.py`, pytest suite, CI gate; active
  `.github/workflows/ci-gate.yml`.
- `api/openapi/registry-api.yaml` (Agent Card Registry API: cards CRUD/search, verify, environments,
  WoA well-known).

### Added (Phase 2)

- `integrations/registry/registry.py`: reference Agent Card Registry implementing
  `api/openapi/registry-api.yaml` (register/search/versions/verify/environments/WoA well-known).
- `tools/cli/spec445.py`: validate / register / verify / search / environments CLI.
- `conformance-kit/runtime-check/verify_integrity.py`: stage-3 startup integrity check.
- CI: `cross-triad` job now runs `crosscheck.py` across the three sibling repos' worked examples.

### Changed (Phase 2 reshape)

- `integrations/registry/` moved to **Agent-Registry** repo (API contract stays canonical here in
  `api/openapi/registry-api.yaml`); `spec445` CLI now targets the registry service.
- Comms pack moved to **agent-standard-docs**; `docs/communication/` is now a pointer.
- `cross-triad` CI job uses **agent-conformance** validators; README/REFERENCES link all service repos.
