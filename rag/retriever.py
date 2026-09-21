"""Retrieval contract for QuantNova AI policy RAG."""

def build_citation(row: dict) -> dict:
    return {
        "policy_id": row.get("policy_id"),
        "title": row.get("title"),
        "section": row.get("section"),
        "version": row.get("version"),
        "snippet": row.get("snippet"),
    }
