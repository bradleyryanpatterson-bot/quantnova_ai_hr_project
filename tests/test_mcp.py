from hr_mcp.client import validate_discovered_tools, REQUIRED_TOOLS

def test_required_mcp_tool_contract():
    assert validate_discovered_tools(REQUIRED_TOOLS)
