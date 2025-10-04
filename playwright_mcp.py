from dotenv import load_dotenv
load_dotenv()
import os
from langchain_google_genai import ChatGoogleGenerativeAI
API_KEY = os.getenv("GEMINI_API_KEY")


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

import asyncio
import json
from typing import List, Dict, Any
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain.agents import AgentExecutor, AgentType
from langchain.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

# MCP Client wrapper for Playwright
class PlaywrightMCPClient:
    def __init__(self):
        self.session = None
        self.client = None
        
    async def connect(self):
        """Connect to the Playwright MCP server
        
        Note: Update the command and args below to match your mcp.json configuration
        """
        import shutil
        import os
        
        # On Windows, we need to use npx.cmd, not npx
        npx_path = shutil.which("npx.cmd")
        
        if not npx_path:
            # Fallback to npx (for non-Windows)
            npx_path = shutil.which("npx")
        
        if not npx_path:
            # Try common Node.js installation paths on Windows
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
        
        # Use the same configuration as your mcp.json
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

# Global MCP client instance
mcp_client = PlaywrightMCPClient()

# Create async wrapper for LangChain
class AsyncToolWrapper:
    def __init__(self, tool_name: str):
        self.tool_name = tool_name
    
    async def arun(self, **kwargs) -> str:
        """Async run method"""
        return await mcp_client.call_tool(self.tool_name, kwargs)
    
    def run(self, **kwargs) -> str:
        """Sync run method - runs async in background"""
        # Get or create event loop
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return loop.run_until_complete(self.arun(**kwargs))

def create_langchain_tool(tool_info: Dict[str, Any]) -> StructuredTool:
    """Convert an MCP tool to a LangChain StructuredTool"""
    tool_name = tool_info["name"]
    schema = tool_info.get("schema", {})
    properties = schema.get("properties", {})
    
    # Create a dynamic Pydantic model for the tool's input
    if properties:
        # Create fields dynamically from schema
        fields = {}
        for prop_name, prop_info in properties.items():
            field_type = str  # Default to string
            description = prop_info.get("description", "")
            fields[prop_name] = (field_type, Field(default="", description=description))
        
        InputModel = type(f"{tool_name}_input", (BaseModel,), {"__annotations__": {k: v[0] for k, v in fields.items()}, **{k: v[1] for k, v in fields.items()}})
    else:
        # Fallback for tools without schema
        class InputModel(BaseModel):
            input: str = Field(default="", description="Tool input")
    
    wrapper = AsyncToolWrapper(tool_name)
    
    return StructuredTool(
        name=tool_name,
        description=tool_info["description"],
        func=wrapper.run,
        coroutine=wrapper.arun,
        args_schema=InputModel
    )

async def run_agent_task(agent_executor, task: str):
    """Run an agent task asynchronously"""
    result = await agent_executor.ainvoke({"input": task})
    return result

async def main():
    # Connect to Playwright MCP server
    print("Connecting to Playwright MCP server...")
    await mcp_client.connect()
    
    # Get available tools
    print("Fetching available tools...")
    mcp_tools = await mcp_client.list_tools()
    print(f"Found {len(mcp_tools)} tools:")
    for tool in mcp_tools:
        print(f"  - {tool['name']}: {tool['description']}")
    
    # Convert MCP tools to LangChain tools
    langchain_tools = [create_langchain_tool(tool) for tool in mcp_tools]
    
    # Initialize LLM (using Gemini)
    llm = ChatGoogleGenerativeAI(api_key=API_KEY,
        model='gemini-2.0-flash-exp',
        temperature=0.0
    )
    
    # Create agent using the new approach - we'll use a custom agent loop
    from langchain.agents import create_structured_chat_agent
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", 
        """You are a helpful AI assistant with access to browser automation tools via Playwright.
        Respond to the human as helpfully and accurately as possible. You have access to the following tools:

        {tools}

        Use a json blob to specify a tool by providing an action key (tool name) 
        and an action_input key (tool input).

        Valid "action" values: "Final Answer" or {tool_names}
        Provide only ONE action per $JSON_BLOB, as shown:
        ```
        {{
        "action": $TOOL_NAME,
        "action_input": $INPUT
        }}
        ```

        Follow this format:

        Question: input question to answer
        Thought: consider previous and subsequent steps
        Action:
        ```
        {{
        "action": $TOOL_NAME,
        "action_input": $INPUT
        }}
        ```
        Observation: action result
        ... (repeat Thought/Action/Observation N times)

        Thought: I know what to respond
        Action:
        ```
        {{
        "action": "Final Answer",
        "action_input": "Final response to human"
        }}
        ```
        Observation: action result
        }}

        ```"""),
        ("human", "{input}\n\n{agent_scratchpad}"),
    ])
    
    agent = create_structured_chat_agent(llm, langchain_tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=langchain_tools, 
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=30
    )

    try:
        result = await run_agent_task(agent_executor, """Navigate to https://www.saucedemo.com/. 
        
        Login using username 'standard_user' and password 'secret_sauce'.
        
        Add the 'Sauce Labs Bike Light' to the cart.
        
        Go to the cart and checkout.
        
        Enter shipping info with first name 'John', last name 'Doe', and postal code '12345'.
        
        Click continue and finish the order.
        
        Click on 'Back Home' to return to the homepage.
        
        click on the menu
        
        Click on 'Logout' to log out of the application.

        Finally, take a screenshot of the homepage and save it as 'final_homepage.png'.
        """)
        print("\nResult:", result.get("output", result))
    except Exception as e:
        print(f"Error: {e}")
    
    # Cleanup
    await mcp_client.disconnect()

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())