"""Optional MCP server exposing local policy and synthetic employee tools."""
from mcp.server.fastmcp import FastMCP
from hr_mcp import tools

mcp = FastMCP("QuantNova AI HR MCP")

@mcp.tool()
def search_policy_documents(query: str, top_k: int = 5) -> dict:
    """Search QuantNova AI policy evidence."""
    return tools.search_policy_documents(query, top_k)

@mcp.tool()
def get_policy_section(policy_id: str, section: str) -> dict:
    """Retrieve one QuantNova AI policy section."""
    return tools.get_policy_section(policy_id, section)

@mcp.tool()
def lookup_employee_profile(employee_id: str) -> dict:
    """Retrieve a synthetic QuantNova AI employee profile."""
    return tools.lookup_employee_profile(employee_id)

@mcp.tool()
def check_pto_balance(employee_id: str) -> dict:
    """Retrieve synthetic QuantNova AI PTO balance."""
    return tools.check_pto_balance(employee_id)

@mcp.tool()
def lookup_benefits_status(employee_id: str) -> dict:
    """Retrieve synthetic QuantNova AI benefits status."""
    return tools.lookup_benefits_status(employee_id)

@mcp.tool()
def create_mock_hr_ticket(employee_id: str, topic: str, summary: str, confirmed: bool = False) -> dict:
    """Create a mock-only QuantNova AI HR ticket after explicit confirmation."""
    if not confirmed:
        return {"status": "confirmation_required", "mock_action": True}
    return {"status": "mock_created", "mock_action": True, "ticket_id": "QNA-TKT-DEMO"}

if __name__ == "__main__":
    mcp.run()
