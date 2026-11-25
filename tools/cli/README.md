# spec445 CLI

`python tools/cli/spec445.py <subcommand>` — validate / register / verify / search / environments
against a card file or a running registry (default `http://localhost:8080`, see
`integrations/registry/`). Validation always runs locally first via
`conformance-kit/validators/card_validate.py`.
