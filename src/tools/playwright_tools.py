from src.mcp_client.playwright_mcp import PlaywrightMCPClient
import asyncio
from pydantic import BaseModel, Field
from langchain.tools import StructuredTool
from typing import List, Dict, Any

# Global MCP client instance
# mcp_client = PlaywrightMCPClient()

# Create async wrapper for LangChain
class AsyncToolWrapper:
    def __init__(self, tool_name: str, mcp_client):
        self.tool_name = tool_name
        self.mcp_client = mcp_client
    
    async def arun(self, **kwargs) -> str:
        """Async run method"""
        return await self.mcp_client.call_tool(self.tool_name, kwargs)

    def run(self, **kwargs) -> str:
        """Sync run method - NOT RECOMMENDED, use async"""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # Create a new event loop in a thread
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, self.arun(**kwargs))
                    return future.result()
            else:
                return loop.run_until_complete(self.arun(**kwargs))
        except Exception as e:
            return f"Error executing tool: {str(e)}"
    
def create_langchain_tool(tool_info: Dict[str, Any], mcp_client) -> StructuredTool:
    """Convert an MCP tool to a LangChain StructuredTool"""
    tool_name = tool_info["name"]
    schema = tool_info.get("schema", {})
    properties = schema.get("properties", {})
    
    # Create a dynamic Pydantic model for the tool's input
    if properties:
        fields = {}
        for prop_name, prop_info in properties.items():
            field_type = str  # Default to string
            description = prop_info.get("description", "")
            fields[prop_name] = (field_type, Field(default="", description=description))
        
        InputModel = type(f"{tool_name}_input", (BaseModel,), {
            "__annotations__": {k: v[0] for k, v in fields.items()}, 
            **{k: v[1] for k, v in fields.items()}
        })
    else:
        class InputModel(BaseModel):
            input: str = Field(default="", description="Tool input")
    
    wrapper = AsyncToolWrapper(tool_name, mcp_client)
    
    return StructuredTool(
        name=tool_name,
        description=tool_info["description"],
        func=wrapper.run,
        coroutine=wrapper.arun,
        args_schema=InputModel
    )