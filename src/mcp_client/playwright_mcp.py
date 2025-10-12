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
import asyncio
from typing import List, Dict, Any
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# MCP Client wrapper for Playwright
class PlaywrightMCPClient:
    def __init__(self):
        self.session = None
        self.client = None
        # Background task and sync primitives used to ensure the stdio
        # async context manager is entered and exited in the same task.
        self._stdio_task: asyncio.Task | None = None
        self._stdio_ready: asyncio.Event | None = None
        self._stdio_stop: asyncio.Event | None = None
        
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
        # Run the stdio_client inside a dedicated asyncio task so that the
        # asynccontextmanager is entered and exited from the same task. This
        # avoids AnyIO errors like "Attempted to exit cancel scope in a
        # different task than it was entered in" which happen when the
        # generator is closed from a different task.
        self._stdio_ready = asyncio.Event()
        self._stdio_stop = asyncio.Event()

        async def _stdio_runner():
            # This coroutine will enter the stdio_client context and keep it
            # open until disconnect requests the runner to stop.
            async with stdio_client(server_params) as (read, write):
                # publish streams to the outer object and signal readiness
                self.read = read
                self.write = write
                if self._stdio_ready:
                    self._stdio_ready.set()
                # wait until stop is set
                if self._stdio_stop:
                    await self._stdio_stop.wait()

        # start the background task and wait until streams are ready
        self._stdio_task = asyncio.create_task(_stdio_runner())
        await self._stdio_ready.wait()

        # create and initialize the client session using the streams
        self.session = ClientSession(self.read, self.write)
        await self.session.__aenter__()
        await self.session.initialize()
        
    async def disconnect(self):
        """Disconnect from the MCP server"""
        # Close the MCP session first
        if self.session:
            try:
                await self.session.__aexit__(None, None, None)
            finally:
                self.session = None

        # Signal the stdio runner to stop and wait for the task to finish.
        if self._stdio_stop and self._stdio_task:
            # notify runner to exit the context manager (it will then __aexit__
            # in the same task that entered it)
            self._stdio_stop.set()
            try:
                await self._stdio_task
            finally:
                self._stdio_task = None
                self._stdio_ready = None
                self._stdio_stop = None
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """List all available tools from the MCP server"""
        response = await self.session.list_tools()
        return [{"name": tool.name, "description": tool.description, "schema": tool.inputSchema} 
                for tool in response.tools]
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Call a tool on the MCP server"""
        result = await self.session.call_tool(tool_name, arguments)
        return json.dumps([item.model_dump() for item in result.content])
