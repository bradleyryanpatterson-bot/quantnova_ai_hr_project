from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="QuantNova AI HR Assistant", version="2.0")

class ChatRequest(BaseModel):
    question: str
    employee_id: str | None = None

@app.get("/health")
def health():
    return {"status": "ok", "app": "QuantNova AI HR Assistant", "mcp": "configured", "index": "configured"}

@app.post("/chat")
def chat(req: ChatRequest):
    # V2 scaffold: agent wiring is implemented in agent/orchestrator.py.
    return {
        "status": "scaffold",
        "answer": "QuantNova AI HR Assistant agent wiring is ready for integration.",
        "citations": [],
        "snippets": [],
        "trace": [{"step": "receive_request", "employee_id": req.employee_id}],
    }

@app.get("/")
def home():
    return {"name": "QuantNova AI HR Assistant", "chat_endpoint": "/chat", "health_endpoint": "/health"}
