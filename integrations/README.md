# integrations

Runtime services live in their own repos in this org — the API contracts stay canonical here:

- **Agent-Registry** — card registry service implementing `api/openapi/registry-api.yaml`
  (moved from `integrations/registry/`): <https://github.com/Agentic-Operation/Agent-Registry>
- **agent-conformance** — canonical validators + triad cross-check + stage-3 runtime check:
  <https://github.com/Agentic-Operation/agent-conformance> (used by the `cross-triad` CI job)

WoA discovery (`/.well-known/woa.json`) and A2A JSON-RPC handler integration notes go here when wired
to the registry service.
