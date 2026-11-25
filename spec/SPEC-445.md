# Spec-445 — AI Agent Card (normative draft v1.0.0-alpha)

**Status:** Draft. **Base:** TM Forum TMF445 v1.0.0 (alpha) — additive extension of the **A2A Agent
Card v1.0**: every A2A-compliant card is a valid Spec-445 card; Spec-445 never modifies A2A base
fields, it adds TM Forum fields via the A2A `extensions` array or as documented additions. Where this
spec and A2A differ, A2A prevails for base fields; Spec-445 prevails for its extensions. Extensions vs
TMF445 are in `annexes/delta-vs-TMF445.md`, marked **[EXT]**.

A card is the machine-readable discovery/interaction contract: identity, classification, capabilities,
skills, data contracts, security, companion refs, lifecycle — published at
`/.well-known/woa.json` (media type `application/woa+json`) for Web-of-Agents discovery.

## §1 Identity [M]

Top-level: `id` [M] (slug; registry key; base must match profile/bootstrap ids), `name` [M] (display),
`description` [M] (1–1024), `version` [M] (semver; MUST match triad), `uuid` [M] (v4; MUST match),
`url` [M] (https base URL; SHOULD match profile §7.2 base_url), `content_identifier_cid` [M for
production], `integrity_wrapper` [R; mandatory regulated] {signature_type, issuer, transparency_log},
`documentationUrl` [O], `iconUrl` [O].

## §2 Classification [M] — `classification` object

`autonomy_level` [M] L1–L5; `agency_class` [M] Agentic AI | Non-Agentic AI (≤L2); `intelligence_class`
[R] (6-value vocab); `automation_role` [M] Worker | Planner | Orchestrator Agent; `mobility` [R]
Static | Single-Environment | Cross-Environment; `oda_relationship` [M] Standalone | Agentified ODA
Component | ODA-Adjacent (drives §6 conditional). All MUST match the Spec-443 profile.

## §3 Capabilities [M] — `capabilities`, `coordination`, `extensions`

`capabilities.streaming` / `pushNotifications` [M], `stateTransitionHistory` [R] (recommended L3+).
`coordination` [TMF addition]: `coordinationProtocol` [R] ∈ a2a_jsonrpc | rep | mcp | wo_a | custom
(matches profile §6.1 / bootstrap §4), `coordinationVariables` [O] (names from profile §6.2),
**[EXT]** `topology_ref` [O] — URL/CID of the profile §6.4 topology block.
`extensions[]` (A2A mechanism): `uri` [M-cond when non-empty], `required` [O], `params`.
**Canonical skillDiscovery extension URI (fixed in Spec-445):**
`https://github.com/tmforum-agents/extensions/skill-discovery/v1` — `params.skillDiscovery` [O] boolean;
`params.discoveryEndpoint` [M-cond when skillDiscovery: true] (https URL). The two are paired.

## §4 Provider [M] — `provider` object

`organization` [M] (MUST equal profile `provider`), `url` [M], `contactEmail` [M] (monitored mailbox —
security-incident channel), `tmForumMemberId` [O], `signingAuthority` [O] (MUST equal
`integrity_wrapper.issuer` when present).

## §5 Skills [M] — `skills[]`

Per skill: `id` [M] = TMF-prefixed taxonomy id (`TMF-OASF <n>` | `TMF-GB1033 F-<n>` |
`EXTENSION-<id>`; string-equality join to profile §4.2 and bootstrap §2 — cross-check C7); `name` [M]
(display; intentionally different from `id`); `description` [M]; `tags` [O]; `examples` [O];
`source_taxonomy` [M] ∈ OASF Skill Taxonomy | GB1033 Functional Framework | TM Forum Custom;
`bound_core_task` [M] (join to profile §4.1 / bootstrap §2, C8); `bound_business_capability` [R]
(GB1022; SHOULD populate when oda_relationship ≠ Standalone); `etom_process_ref` [R] (GB921 L2/L3).

## §6 Inputs, Outputs & Data Contracts [M-cond] — `defaultInputModes`, `defaultOutputModes`, `defaultDataContracts`

A2A base arrays of MIME types [M]. **[M-cond]** `defaultDataContracts` required when
`oda_relationship` ≠ Standalone (never an empty array — omit instead): per entry `format` ∈
tmforum-sid | openapi | json-schema | custom, `schemaRef` [M], `entities` [R] (SID), `tmForumApiRef`
[R] (name + version; joins to profile §5.2 / bootstrap §3, C9), `role` [O] input | output | both.

## §7 Authentication & Security [M] — `authentication`, `deonticConstraints`, `impactRadius`

`authentication.schemes` [M] ∈ oauth2_oidc | mtls | api_key | bearer | basic | custom (MUST match
profile §8.3 / bootstrap §5, C13); `credentials` [M] ∈ header | query | cookie | mtls_cert;
`scopesRequired` [O]; `tokenValidation` [R] ∈ jwks_uri | introspection | static_jwk; `issuer` [R,
required for oauth2_oidc]; `audience` [O]. `deonticConstraints` [TMF]: `embargoes` [R], `burdens` [R]
(ODP-EL tokens matching profile §8.1, C14; empty arrays non-conformant at L3+). `impactRadius` [M] ∈
low | medium | high (MUST match profile §8.4, C15).

## §8 Companion Artifacts [M] — `spec443_profile_ref`, `spec444_bootstrap_ref`, `companionArtifacts[]`

`spec443_profile_ref` [M]; `spec444_bootstrap_ref` [M-cond: bootstrap exists]; pointers MUST be
bidirectional (C18). `companionArtifacts[]` [O] extra {role, ref} pairs.

## §9 Lifecycle [M] — `deploymentStatus`, `lastUpdated`, `maintenancePlan`, `autonomyCaseRef`

`deploymentStatus` [M] ∈ draft | in_review | approved | deprecated (SHOULD match cover-block status);
`lastUpdated` [M] ISO 8601; `maintenancePlan` [R] (matches profile §10.4); `documentation[]` [O];
`autonomyCaseRef` [M-cond: L3+] (matches profile §10.4 / bootstrap post_bootstrap hook, C17).

## §10 Validation [M] (procedural)

Three stages: (1) pre-commit — JSON Schema (`schemas/agent-card.schema.json`, Annex B normative) +
secret-leak detector; (2) CI gate — schema + triad cross-check (`annexes/cross-check-manifest.md`) +
extension-URI validator; (3) runtime — `integrity_wrapper` signature vs transparency log at startup.
Controlled vocabularies as in §1–§9; all URLs https; uuid v4; semver.

## [EXT] Spec-445 extensions (in the A2A `extensions[]` array)

### E1 environment-instances — URI `https://github.com/tmforum-agents/extensions/environment-instances/v1`

```json
{"uri": "https://github.com/tmforum-agents/extensions/environment-instances/v1", "required": false,
 "params": {"environments": [
   {"environment": "prod", "instance_id": "lma-prod-7f3c9d", "deploymentStatus": "approved",
    "deployed_version": "1.0.0-stable", "artifact_cid": "sha256:...", "card_cid": "sha256:...",
    "url": "https://agents.example.com", "health": "healthy", "last_check": "2026-11-25T00:00:00Z",
    "rollout_state": "active", "autonomyCaseRef": "https://grc.example.com/.../prod"}]}}
```

[M-cond: mobility ≠ Static] Environment names MUST match bootstrap `environments[]` and profile §10.1a
(C20). Mirrors the Spec-444 §6.3 inventory record from the discovery side.

### E2 modelGovernance — URI `https://github.com/tmforum-agents/extensions/model-governance/v1`

```json
{"uri": "https://github.com/tmforum-agents/extensions/model-governance/v1", "required": false,
 "params": {"models": [{"model_id": "churn-scorer", "version": "2.3.1", "cid": "sha256:...",
                        "risk_class": "medium", "authority_endpoint": "https://models.example.com/v1/models"}]}}
```

[M-cond: any model-bound skill] MUST match bootstrap `model_bindings` and profile §3.1/§9.2 (C19).

## Annexes

- `annexes/delta-vs-TMF445.md`, `annexes/cross-check-manifest.md`, `annexes/self-check.md`
- `schemas/agent-card.schema.json` — normative JSON Schema (additive over A2A)
- Worked example: `../examples/loyalty-agent/card.json`
