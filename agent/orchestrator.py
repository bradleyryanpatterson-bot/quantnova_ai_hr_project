"""QuantNova AI agent orchestration scaffold.

User-visible traces contain operational events only and never hidden chain-of-thought.
"""
from dataclasses import dataclass, field

@dataclass
class AgentState:
    employee_id: str | None
    intent: str = "unknown"
    sources: list[dict] = field(default_factory=list)
    trace: list[dict] = field(default_factory=list)
    requires_confirmation: bool = False

READ_TOOLS = {"search_policy_documents", "get_policy_section", "lookup_employee_profile", "check_pto_balance", "lookup_benefits_status", "web_search"}
WRITE_TOOLS = {"create_mock_hr_ticket"}

def safe_trace(tool: str, args: dict, status: str, source: str | None = None) -> dict:
    return {"tool": tool, "args": args, "status": status, "source": source}

def requires_confirmation(tool: str) -> bool:
    return tool in WRITE_TOOLS
