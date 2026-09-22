# QuantNova AI HR Assistant

A working local HR demo with a browser chat page, policy citations, vacation calculations, and synthetic employee benefit lookups. All employees, policies, and records are fictional.

## Run on Windows

From this project folder, run:

```powershell
.\start-local.cmd
```

Or double-click `start-local.cmd`. The launcher creates `.venv` if needed, installs the minimal runtime when missing, and starts the server on port 8080. Python 3.10 or newer must be installed and available through `py` for first-time setup.

Open http://127.0.0.1:8080/ for the chat page. Keep the terminal open; press Ctrl+C to stop.

If port 8080 is occupied, either use the already-running app or run `start-local.cmd 8081` and open http://127.0.0.1:8081/. The launcher binds only to this machine. Port 8000 produced Windows error 10013 on the development machine, so 8080 is the default.

## Manual setup

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-local.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8080
```

No environment activation, database, API key, or model download is required for local mode. On macOS/Linux, use `python3 -m venv .venv` and `.venv/bin/python` in the commands above.

## What works

- Browser chat with demo employee selection, expandable citations, full policy links, and tool traces.
- Section-based keyword search across eight Markdown policies (50 sections).
- Vacation balance estimates from the checked-in PTO records, with eight-hour workdays and explicit manager approval guidance.
- Benefit enrollment from the checked-in records, separate from policy eligibility.
- Missing-record handling, employee-ID mismatch detection, and input validation.
- `/health` checks that policy and employee data can be loaded. `/docs` provides interactive API documentation.
- The optional MCP server shares the same five functional read tools: install `mcp` and run `python -m hr_mcp.server` to expose them over stdio. The web app calls these handlers in process; it does not launch an MCP connection.

## Try it

Select Maya Chen (QNA-1001): “Can I take five vacation days, and what would my balance be afterward?” The recorded 96 hours minus 40 hours gives an estimated 56 hours remaining.

Select Jordan Lee (QNA-1002): “What benefits am I enrolled in and am I eligible?” The response shows the temporary classification, recorded enrollment, and relevant policy.

Choose General policy question: “How do I raise a workplace concern?”

## Current boundaries

This mode uses deterministic workflows and retrieved policy excerpts, not a generative language model. Each question is independent, with no conversation memory. Record dates are shown because the data is a fixed snapshot. Demo identity selection is not authentication; use only the supplied fictional data and keep the server local.

The web app does not submit tickets, approve leave, or change records. The optional MCP ticket tool only returns a mock acknowledgement after confirmation; it does not persist a ticket. PostgreSQL, pgvector, LangChain orchestration, external search, and model-provider integration remain future work. The legacy `db.init_db` and `rag.ingest` commands are scaffold utilities and are not required for local startup. The original `requirements.txt` retains those broader integration dependencies; use `requirements-local.txt` for this app.

## Tests

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-local.txt
.\.venv\Scripts\python.exe -m pytest -q
```
