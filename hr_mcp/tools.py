"""Shared local handlers for the web app and optional MCP server."""
import json
from pathlib import Path
from rag.retriever import search, sections

DATA = Path(__file__).resolve().parents[1] / 'mock_data'

def records(name):
    return json.loads((DATA / f'{name}.json').read_text(encoding='utf-8'))

def lookup(name, employee_id):
    row = next((r for r in records(name) if r['employee_id'] == employee_id.upper()), None)
    return {'status': 'ok' if row else 'not_found', 'record': row, 'source': f'mock_data/{name}.json'}

def lookup_employee_profile(employee_id: str) -> dict:
    return lookup('employees', employee_id)

def check_pto_balance(employee_id: str) -> dict:
    return lookup('pto', employee_id)

def lookup_benefits_status(employee_id: str) -> dict:
    return lookup('benefits', employee_id)

def search_policy_documents(query: str, top_k: int = 5) -> dict:
    return {'status': 'ok', 'results': search(query, top_k)}

def get_policy_section(policy_id: str, section: str) -> dict:
    row = next((r for r in sections() if r['policy_id'] == policy_id and r['section'].lower() == section.lower()), None)
    return {'status': 'ok' if row else 'not_found', 'record': row}
