# Agent Discovery Card (Spec-445): The AI Agent Card

**Spec-445** is the *source/discover* contract of the agent triad: a machine-readable JSON **Agent Card**,
additive over the **A2A Agent Card v1.0** (every A2A-compliant card is a valid Spec-445 card), used for
registry lookup, WoA discovery at `/.well-known/woa.json`, A2A invocation, and integrity verification.

Spec-445 extensions over TM Forum **TMF445 v1.0.0** (alpha; delta in `spec/annexes/delta-vs-TMF44X.md`):
`environment-instances` (per-environment instance registration), `modelGovernance` (bound model
id/version/CID/risk class), topology reference in `coordination`, and a single canonical skillDiscovery URI.

- **Status:** Draft — `spec/SPEC-445.md` v1.0.0-alpha merged on `main` (PRs #1–#3); comms pack canonical in [agent-standard-docs](https://github.com/Agentic-Operation/agent-standard-docs). **License:** Apache-2.0

## The triad (sibling repos)

| Verb | Spec | Repo |
|---|---|---|
| Define | Spec-443 | [`agent-profile-management`](https://github.com/Agentic-Operation/agent-profile-management) |
| Onboard | Spec-444 | [`agent-bootstrap-management`](https://github.com/Agentic-Operation/agent-bootstrap-management) |
| **Source** (this repo) | Spec-445 | `Agentic-Operation/agent-discovery-card` |

Join keys across the triad: identity fields (`id`, `uuid`, `version`, `provider`, CID, `integrity_wrapper`),
`skills[].id` string equality (`TMF-OASF <n>` / `TMF-GB1033 F-xxxx`), bidirectional companion pointers —
see the [triad overview](https://github.com/Agentic-Operation/agent-standard-docs/blob/main/communication/00-triad-overview.md) in agent-standard-docs.

## Repository map

| Directory | Purpose |
|---|---|
| `spec/` | Normative Spec-445 text + annexes (JSON Schema annex, cross-check manifest, self-check) |
| `schemas/agent-card.schema.json` | Normative card schema (additive over A2A) + valid/invalid test vectors |
| `examples/loyalty-agent/` | Worked example `card.json` incl. environment instances |
| `conformance-kit/` | JSON Schema validator, Annex-C cross-check, CI templates, runtime integrity check |
| `api/openapi/` | **Agent Card Registry API** — register/get/search cards, WoA resolution, integrity verify, env-instance registration |
| `tools/cli/` | `spec445 validate/register/verify` CLI |
| `integrations/` | WoA/HAIDIP discovery, A2A JSON-RPC handler, registry backend, Sigstore verify |
| `user-tools/` | Client SDKs (python/ts), card examples, Postman collection |
| `docs/communication/` | Pointer to the canonical comms pack in [agent-standard-docs](https://github.com/Agentic-Operation/agent-standard-docs) |
| `docs/guides/` `docs/architecture/` `docs/references/` | Quickstarts, diagrams, related sources |

## Quickstart

See [docs/guides/quickstart-publish-a-card.md](docs/guides/quickstart-publish-a-card.md) and the
[03-source-and-discover](https://github.com/Agentic-Operation/agent-standard-docs/blob/main/communication/03-source-and-discover.md) one-pager in agent-standard-docs.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Branch convention `vibe/<slug>-5a1ad6`, draft PRs.

## Runtime services (this org)

| Service | Repo |
|---|---|
| Agent Card Registry (this repo's API) | [Agent-Registry](https://github.com/Agentic-Operation/Agent-Registry) |
| Model Management Authority | [model-authority](https://github.com/Agentic-Operation/model-authority) |
| Rollout controller | [agent-rollout-controller](https://github.com/Agentic-Operation/agent-rollout-controller) |
| Orchestrator (swarm/hierarchy) | [agent-orchestrator](https://github.com/Agentic-Operation/agent-orchestrator) |
| Tool & MCP manager | [tool-mcp-manager](https://github.com/Agentic-Operation/tool-mcp-manager) |
| Conformance kit (validators, cross-check C1–C20, stage-3 check) | [agent-conformance](https://github.com/Agentic-Operation/agent-conformance) |
| Published docs / comms pack (canonical) | [agent-standard-docs](https://github.com/Agentic-Operation/agent-standard-docs) |
