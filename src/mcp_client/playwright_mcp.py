# Playwright MCP + LangChain Agent Integration
# 
# INSTALLATION STEPS:
# 
# 1. Install Node.js and npm (required for Playwright MCP):
#    - Download from: https://nodejs.org/
#    - Verify: node --version && npm --version
#
# 2. Install Playwright MCP Server:
#    npm install -g @playwright/mcp
#    # Or use npx (no installation needed): npx -y @playwright/mcp
#
# 3. Install Python dependencies:
#    pip install langchain langchain-google-genai langchain-community mcp google-generativeai
#
# 3. Set your API key:
#    export GOOGLE_API_KEY='your-api-key-here'
#    # Or on Windows: set GOOGLE_API_KEY=your-api-key-here

import json
from typing import List, Dict, Any
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# MCP Client wrapper for Playwright
class PlaywrightMCPClient:
    def __init__(self):
        self.session = None
        self.client = None
        
    async def connect(self):
        """Connect to the Playwright MCP server"""
        import shutil
        import os
        
        # On Windows, we need to use npx.cmd, not npx
        npx_path = shutil.which("npx.cmd")
        
        if not npx_path:
            npx_path = shutil.which("npx")
        
        if not npx_path:
            possible_paths = [
                os.path.expandvars(r"%APPDATA%\npm\npx.cmd"),
                r"C:\Program Files\nodejs\npx.cmd",
                r"C:\Program Files (x86)\nodejs\npx.cmd",
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    npx_path = path
                    break
        
        if not npx_path:
            raise RuntimeError(
                "npx.cmd not found. Please:\n"
                "1. Install Node.js from https://nodejs.org/\n"
                "2. Restart your terminal\n"
                "3. Verify with: npx --version"
            )
        
        print(f"Using npx at: {npx_path}")
        
        server_params = StdioServerParameters(
            command=npx_path,
            args=["@playwright/mcp@latest"],
            env=None
        )
        
        self.client = stdio_client(server_params)
        self.read, self.write = await self.client.__aenter__()
        self.session = ClientSession(self.read, self.write)
        await self.session.__aenter__()
        await self.session.initialize()
        
    async def disconnect(self):
        """Disconnect from the MCP server"""
        if self.session:
            await self.session.__aexit__(None, None, None)
        if self.client:
            await self.client.__aexit__(None, None, None)
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """List all available tools from the MCP server"""
        response = await self.session.list_tools()
        return [{"name": tool.name, "description": tool.description, "schema": tool.inputSchema} 
                for tool in response.tools]
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Call a tool on the MCP server"""
        result = await self.session.call_tool(tool_name, arguments)
        return json.dumps([item.model_dump() for item in result.content])
