from dotenv import load_dotenv
load_dotenv()
import os
from langchain_openai import ChatOpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

from prompt.prompts import system_prompt
from src.mcp_client.playwright_mcp import PlaywrightMCPClient
from src.tools.playwright_tools import create_langchain_tool
from langchain.agents import AgentExecutor
from src.tools.editor_tools import get_writer_tool
from src.tools.get_user_story_tool import create_work_items_tool

# Global MCP client instance
mcp_client = PlaywrightMCPClient()

async def run_agent_task(agent_executor, task: str):
    """Run an agent task asynchronously"""
    result = await agent_executor.ainvoke({"input": task})
    return result

async def test_agent(testing_prompt):
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
    langchain_tools = [create_langchain_tool(tool, mcp_client) for tool in mcp_tools]
    editor_tool = [get_writer_tool()]
    azdo_tool = [create_work_items_tool()]
    
    # Initialize LLM - Use ChatOpenAI with proper configuration
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.0,
        openai_api_key=OPENAI_API_KEY
    )
    
    # Use the OpenAI Functions agent instead of structured chat
    from langchain.agents import create_openai_functions_agent
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    agent = create_openai_functions_agent(llm, langchain_tools+editor_tool+azdo_tool, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=langchain_tools+editor_tool+azdo_tool,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=20,
        return_intermediate_steps=True
    )

    try:
        result = await agent_executor.ainvoke({"input": testing_prompt})
        print("\nResult:", result.get("output", result))
        return result
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Cleanup
    await mcp_client.disconnect()