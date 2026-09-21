# QuantNova AI HR Assistant - V2

QuantNova AI HR Assistant is a fictional employee-support application for policy Q&A and guided HR workflows. All employee records, balances, benefit records, tickets, policy identifiers, and organizational details in this repository are synthetic and belong only to the fictional company QuantNova AI.

## V2 baseline
- Responsive chat UI plus JSON `/chat` and `/health` endpoints.
- LangChain-oriented agent orchestration with explicit tool routing.
- MCP client/server boundary with at least five HR tools.
- PostgreSQL + pgvector for policy chunks, metadata, and synthetic HR data.
- Policy RAG with traceable citations and source snippets.
- PTO Guidance and Benefits Guidance multi-step workflows.
- Optional external web search through Tavily with DuckDuckGo fallback; external results are never treated as QuantNova AI policy.
- Short operational trace containing tool names, safe arguments, results, and sources; no hidden model reasoning.
- CI tests for application startup, policy retrieval, and MCP discovery/calls.

## Core architecture
User -> Web/API -> LangChain Agent -> MCP Client -> MCP Server -> PostgreSQL/pgvector -> QuantNova AI policy + synthetic HR records -> grounded answer/citations.

## Quick start
1. Create a virtual environment and install `requirements.txt`.
2. Copy `.env.example` to `.env` and fill in provider/database credentials.
3. Start PostgreSQL with pgvector and run `python -m db.init_db`.
4. Run `python -m rag.ingest` to index QuantNova AI policies.
5. Start the app with `uvicorn app.main:app --reload`.
6. Open `http://localhost:8000`.

## Demo identities
Use only synthetic QuantNova AI employee IDs such as `QNA-1001` and `QNA-1002`.

## Demo workflow 1 - PTO
"I'm QNA-1001. Can I take five vacation days next month, and what would my balance be afterward?"

Expected tool sequence: employee profile -> PTO balance -> policy search/section -> calculation -> cited guidance. Any request submission remains a mock action and requires explicit confirmation.

## Demo workflow 2 - Benefits
"I'm QNA-1002, a temporary employee. What benefits am I currently enrolled in, and what does QuantNova AI policy say about eligibility?"

Expected tool sequence: employee profile -> benefits status -> employment-classification policy -> benefits policy -> cited guidance or HR referral if evidence is insufficient.

## Safety
The model is not the authority for QuantNova AI HR facts. Policy documents and approved MCP tool results are the authoritative evidence for this demo. Missing, conflicting, or unavailable evidence must be surfaced rather than invented.
