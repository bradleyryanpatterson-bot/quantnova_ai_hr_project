"""MCP client integration boundary for QuantNova AI HR Assistant."""

REQUIRED_TOOLS = [
    "search_policy_documents",
    "get_policy_section",
    "lookup_employee_profile",
    "check_pto_balance",
    "lookup_benefits_status",
]

def validate_discovered_tools(tool_names: list[str]) -> bool:
    return all(name in tool_names for name in REQUIRED_TOOLS)
