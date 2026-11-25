# Delta annex — Spec-445 vs TMF445 v1.0.0

| Spec-445 location | Extension / fix | TMF445 origin | Class | Rationale |
|---|---|---|---|---|
| Front Matter | companion refs renamed `spec443_profile_ref` / `spec444_bootstrap_ref` | TMF445 Front Matter | [M] | align with Spec-44X |
| §3 | **single canonical skillDiscovery URI** `https://github.com/tmforum-agents/extensions/skill-discovery/v1` (TMF445 named two conflicting URIs) | TMF445 §3 | [M-cond] | one namespace, no ambiguity |
| §3 `coordination` | `topology_ref` pointer to the Spec-443 §6.4 topology block | TMF445 §3 (protocol + variables only) | [O] | machine-readable swarm/hierarchy on the card |
| §9 / E1 | `environment-instances` extension: per-environment instance registration (environment, instance_id, status, deployed_version, CIDs, url, health, rollout_state, per-env autonomyCaseRef) | TMF445 §9 (single deploymentStatus) | [M-cond: mobility ≠ Static] | per-environment discovery state |
| E2 | `modelGovernance` extension: bound models (id/version/CID/risk class/authority endpoint) | none in TMF445 | [M-cond: model-bound skill] | sourcing-time model governance; joins to bootstrap §2.2 (C19) |
| §10 | cross-check manifest extended with C19/C20 | TMF445 §10 / Annex C | [M] | triad joins incl. new extensions |

Carried-over fixes: worked-example version consistency (example uses one version everywhere), the
"not a real" URI placeholder removed in favour of the canonical one above.
