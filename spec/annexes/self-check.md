# Pre-submission self-check (Spec-445 card)

- [ ] All [M] fields present: id, name, description, version, uuid, url, provider (organization/url/contactEmail), classification (autonomy_level, agency_class, automation_role, oda_relationship), capabilities.streaming/pushNotifications, authentication.schemes/credentials, defaultInputModes/OutputModes, skills (id, name, description, source_taxonomy, bound_core_task), impactRadius, deploymentStatus, lastUpdated, spec443_profile_ref.
- [ ] Conditional: defaultDataContracts (oda_relationship ≠ Standalone, non-empty), spec444_bootstrap_ref (bootstrap exists), autonomyCaseRef (L3+), extensions[].uri (non-empty extensions), discoveryEndpoint (skillDiscovery: true).
- [ ] Skill IDs carry the TMF prefix exactly; every skill bound to a profile core task.
- [ ] skillDiscovery URI is the canonical one; discoveryEndpoint paired.
- [ ] [EXT] environment-instances present when mobility ≠ Static; environment names match bootstrap environments[] (C20).
- [ ] [EXT] modelGovernance present when any skill uses a model adapter; matches bootstrap model_bindings (C19).
- [ ] deonticConstraints non-empty at L3+; impactRadius matches profile §8.4.
- [ ] Companion refs bidirectional (C18).
- [ ] `card_validate.py` + schema + `crosscheck.py` pass; A2A base validation also passes (additive rule).
