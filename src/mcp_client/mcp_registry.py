import json
from mcp_registry import ServerRegistry, MCPAggregator, get_config_path

async def get_mcp_client():
    """Create and return an MCP client connected to the aggregator"""
    # Connect to MCP registry and aggregator
    print("Connecting to MCP registry and aggregators...")
    registry = ServerRegistry.from_config(get_config_path())

    async with MCPAggregator(registry) as aggregator:
        # Discover tools via aggregator
        results = await aggregator.list_tools()
        mcp_tools = [
            {"name": t.name, "description": t.description or "", "schema": t.inputSchema or {}}
            for t in results.tools
        ]
        print(f"Found {len(mcp_tools)} tools:")
        for tool in mcp_tools:
            print(f"  - {tool['name']}: {tool['description']}")

        # Adapter to match existing PlaywrightMCPClient.call_tool shape
        class AggregatorClient:
            def __init__(self, aggregator):
                self.aggregator = aggregator

            async def call_tool(self, tool_name: str, arguments: dict) -> str:
                res = await self.aggregator.call_tool(tool_name, arguments)
                # Try to convert MCP return items to JSON similar to Playwright client
                try:
                    return json.dumps([item.model_dump() for item in res.content])
                except Exception:
                    return json.dumps(res.content if hasattr(res, "content") else res)

        mcp_client = AggregatorClient(aggregator)
        return mcp_client, mcp_tools