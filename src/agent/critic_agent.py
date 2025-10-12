from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
import os
from langchain_openai import ChatOpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

from langchain.agents import AgentExecutor
from src.tools.editor_tools import get_writer_tool, get_reader_tool
from src.tools.get_user_story_tool import create_work_items_tool
from langchain_community.callbacks import get_openai_callback
from prompt.prompts import EVALUATION_SYSTEM_PROMPT, evaluation_task

async def run_evaluation_agent(evaluation_prompt):
    """
    Run the evaluation agent to analyze the test execution process
    
    Args:
        evaluation_prompt: The task description for evaluation
    """
    
    # Initialize tools
    reader_tool = get_reader_tool()
    writer_tool = get_writer_tool()
    azdo_tool = create_work_items_tool()
    
    tools = [reader_tool, writer_tool, azdo_tool]
    
    # Initialize LLM
    llm = ChatOpenAI(
        model="gpt-4o",  # Using more capable model for evaluation
        temperature=0.0,
        openai_api_key=OPENAI_API_KEY
    )
    
    # Create agent with OpenAI Functions
    from langchain.agents import create_openai_functions_agent
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", EVALUATION_SYSTEM_PROMPT),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    agent = create_openai_functions_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=20,
        return_intermediate_steps=True
    )

    try:
        cost_details = ""
        with get_openai_callback() as cb:
            print("\n" + "="*60)
            print("STARTING EVALUATION AGENT")
            print("="*60 + "\n")
            
            result = await agent_executor.ainvoke({"input": evaluation_prompt})
            
            cost_details += f"""
            {"-"*20}
            Evaluation Agent Execution Time: {datetime.now().isoformat()}
            Total Tokens: {cb.total_tokens}
            Prompt Tokens: {cb.prompt_tokens}
            Completion Tokens: {cb.completion_tokens}
            Total Cost (USD): ${cb.total_cost}
            {"-"*20}
            """
            
            with open("evaluation_cost_details.txt", "w", encoding="utf-8") as f:
                f.write(cost_details)
            
            print("\n" + "="*60)
            print("EVALUATION COMPLETED")
            print("="*60)
            print("\nResult:", result.get("output", result))
            print("\nCost Details:")
            print(cost_details)
            
            return result
            
    except Exception as e:
        print(f"Error during evaluation: {e}")
        import traceback
        traceback.print_exc()
        return None


async def main():
    """Main function to run the evaluation agent"""    
    result = await run_evaluation_agent(evaluation_task)
    
    if result:
        print("\n✅ Evaluation completed successfully!")
        print("📄 Check 'evaluation.html' for the detailed report")
    else:
        print("\n❌ Evaluation failed")


# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(main())