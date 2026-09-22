from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, PlainTextResponse
from pydantic import BaseModel, Field
from agent.orchestrator import answer_question
from hr_mcp.tools import records
from rag.retriever import sections
from rag.ingest import policy_files

app = FastAPI(title="QuantNova AI HR Assistant", version="2.0")

class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=4000)
    employee_id: str | None = Field(default=None, pattern=r'^QNA-\d{4}$')

@app.get("/health")
def health():
    try:
        count = len(sections())
        employees = len(records('employees'))
        records('pto')
        records('benefits')
        if not count or not employees:
            raise ValueError('Empty local data')
        return {'status': 'ok', 'app': 'QuantNova AI HR Assistant', 'mode': 'local_grounded',
                'policy_sections': count, 'employees': employees, 'tools': 'in_process',
                'model': 'not_used', 'database': 'not_used'}
    except (OSError, ValueError, AttributeError):
        raise HTTPException(503, 'Local policy or employee data is unavailable or invalid.')

@app.post("/chat")
def chat(req: ChatRequest):
    if not req.question.strip():
        raise HTTPException(422, 'Enter a question.')
    try:
        return answer_question(req.question.strip(), req.employee_id)
    except (OSError, ValueError, AttributeError):
        raise HTTPException(503, 'Local data could not be read. Check /health and the project data files.')

@app.get("/")
def home():
    return FileResponse(Path(__file__).with_name('index.html'))

@app.get('/employees')
def employees():
    return [{'employee_id': row['employee_id'], 'name': f"{row['first_name']} {row['last_name']}",
             'employment_type': row['employment_type']} for row in records('employees')]

@app.get('/policies/{filename}', response_class=PlainTextResponse)
def policy(filename: str):
    path = next((p for p in policy_files() if p.name == filename), None)
    if path is None:
        raise HTTPException(404, 'Policy not found')
    return path.read_text(encoding='utf-8')
