# Deployment Record - QuantNova AI HR Assistant

## Public URL
To be added after deployment.

## Health URL
`<PUBLIC_BASE_URL>/health`

## Deployment checklist
- CI tests pass before deployment.
- PostgreSQL/pgvector is reachable.
- QuantNova AI policy index is populated.
- Synthetic HR seed data is loaded.
- MCP discovery and a simple read-only tool call pass.
- Secrets are environment variables only.
- Cold-start behavior is documented.
- Public demo contains no real employee or non-QuantNova organizational data.
