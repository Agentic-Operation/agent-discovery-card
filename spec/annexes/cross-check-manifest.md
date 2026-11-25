# Cross-check manifest — Spec-445 side

Full triad manifest (C1–C20) canonical in
`agent-profile-management/spec/annexes/cross-check-manifest.md`. Card-side joins enforced by
`conformance-kit/validators/card_validate.py` + `crosscheck.py`:

- C1–C6: `id`/`uuid`/`version`/`provider.organization`/`content_identifier_cid`/`integrity_wrapper` ≡ profile ≡ bootstrap.
- C7/C8: `skills[*].id` and `bound_core_task` ≡ profile §4.2/§4.1 ≡ bootstrap `skill_bindings`.
- C9: `defaultDataContracts[*].tmForumApiRef` join to profile §5.2 and bootstrap `tool_bindings`.
- C10/C11: `coordination.coordinationProtocol` / `coordinationVariables` match profile §6.1/§6.2; C12: `coordination.topology_ref` points at profile §6.4.
- C13: `authentication.schemes` consistent with profile §8.3 and bootstrap `security_config.auth.provider`.
- C14/C15: `deonticConstraints` ⊇ profile §8.1 tokens; `impactRadius` = profile §8.4.
- C17: `autonomyCaseRef` present at L3+, matches profile §10.4 and bootstrap post_bootstrap artifact.
- C18: `spec443_profile_ref` / `spec444_bootstrap_ref` bidirectional.
- C19 [EXT]: `modelGovernance` models ≡ bootstrap `model_bindings` ≡ profile §3.1/§9.2.
- C20 [EXT]: `environment-instances` environments ≡ bootstrap `environments[]` ≡ profile §10.1a.
