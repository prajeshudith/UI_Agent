"""
pip install langchain langchain-google-genai playwright python-dotenv
playwright install chromium

https://ultimateqa.com/dummy-automation-websites/
"""

from dotenv import load_dotenv
load_dotenv()
import os
import time
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool, BaseTool
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from pydantic import BaseModel, Field

from playwright.sync_api import sync_playwright, Page, Browser
from playwright.sync_api import TimeoutError as PlaywrightTimeout

# Initialize LLM
API_KEY = os.getenv("GEMINI_API_KEY")
llm = ChatGoogleGenerativeAI(api_key=API_KEY, model='gemini-2.0-flash-exp', temperature=0.3)

# Browser Manager Class
class BrowserManager:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None
        self.context = None
        
    def start(self):
        if not self.playwright:
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=False)
            self.context = self.browser.new_context(
                viewport={'width': 1280, 'height': 720},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            self.page = self.context.new_page()
            self.page.set_default_timeout(10000)
            
    def stop(self):
        if self.page:
            self.page.close()
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
            
    def get_page(self) -> Page:
        if not self.page:
            self.start()
        return self.page

# Global browser manager instance
browser_manager = BrowserManager()

# Tool Classes
class NavigateTool(BaseTool):
    name: str = "navigate_to_url"
    description: str = "Navigate to a specific URL. Input should be a valid URL starting with http:// or https://"
    
    def _run(self, url: str) -> str:
        try:
            page = browser_manager.get_page()
            page.goto(url, wait_until="domcontentloaded")
            time.sleep(2)
            return f"Successfully navigated to {url}"
        except Exception as e:
            return f"Error navigating to {url}: {str(e)}"
    
    async def _arun(self, url: str) -> str:
        raise NotImplementedError

class ClickElementTool(BaseTool):
    name: str = "click_element"
    description: str = "Click on an element. Input can be text content, CSS selector, or XPath"
    
    def _run(self, selector: str) -> str:
        try:
            page = browser_manager.get_page()
            
            # Try different selector strategies
            if selector.startswith('//'):
                page.click(selector)
            elif selector.startswith('.') or selector.startswith('#'):
                page.click(selector)
            else:
                # Try to click by text
                page.click(f"text={selector}")
                
            time.sleep(1)
            return f"Successfully clicked element: {selector}"
        except Exception as e:
            return f"Error clicking element {selector}: {str(e)}"
    
    async def _arun(self, selector: str) -> str:
        raise NotImplementedError

class TypeTextTool(BaseTool):
    name: str = "type_text"
    description: str = "Type text into an input field. Format: 'selector|text'. Example: '#search|flight tickets'"
    
    def _run(self, input_str: str) -> str:
        try:
            parts = input_str.split('|', 1)
            if len(parts) != 2:
                return "Error: Input should be in format 'selector|text'"
            
            selector, text = parts
            page = browser_manager.get_page()
            
            # Clear existing text first
            page.fill(selector, "")
            page.type(selector, text, delay=50)
            
            return f"Successfully typed '{text}' into {selector}"
        except Exception as e:
            return f"Error typing text: {str(e)}"
    
    async def _arun(self, input_str: str) -> str:
        raise NotImplementedError

class ExtractElementsTool(BaseTool):
    name: str = "extract_elements"
    description: str = "Extract text content from elements matching a selector"
    
    def _run(self, selector: str) -> str:
        try:
            page = browser_manager.get_page()
            elements = page.query_selector_all(selector)
            
            if not elements:
                return f"No elements found for selector: {selector}"
            
            texts = []
            for i, elem in enumerate(elements[:10], 1):
                text = elem.text_content()
                if text and text.strip():
                    texts.append(f"{i}. {text.strip()}")
            
            return "\n".join(texts) if texts else "Elements found but no text content"
        except Exception as e:
            return f"Error extracting elements: {str(e)}"
    
    async def _arun(self, selector: str) -> str:
        raise NotImplementedError

class GetPageInfoTool(BaseTool):
    name: str = "get_page_info"
    description: str = "Get current page title, URL, and visible text summary"
    
    def _run(self, _: str = "") -> str:
        try:
            page = browser_manager.get_page()
            title = page.title()
            url = page.url
            
            # Get main visible text
            text_content = page.evaluate("""
                () => {
                    const elements = document.querySelectorAll('h1, h2, h3, p, a, button, input[type="submit"]');
                    const texts = Array.from(elements).slice(0, 20).map(el => el.innerText || el.value).filter(t => t && t.trim());
                    return texts.join(' | ');
                }
            """)
            
            return f"Title: {title}\nURL: {url}\nContent preview: {text_content[:500]}"
        except Exception as e:
            return f"Error getting page info: {str(e)}"
    
    async def _arun(self, _: str) -> str:
        raise NotImplementedError

class WaitTool(BaseTool):
    name: str = "wait"
    description: str = "Wait for specified seconds. Input should be a number between 1-10"
    
    def _run(self, seconds: str) -> str:
        try:
            wait_time = min(10, max(1, int(seconds)))
            time.sleep(wait_time)
            return f"Waited for {wait_time} seconds"
        except Exception:
            return "Error: Please provide a valid number of seconds (1-10)"
    
    async def _arun(self, seconds: str) -> str:
        raise NotImplementedError

class ScrollTool(BaseTool):
    name: str = "scroll"
    description: str = "Scroll the page. Input: 'down', 'up', or 'bottom'"
    
    def _run(self, direction: str) -> str:
        try:
            page = browser_manager.get_page()
            
            if direction.lower() == "down":
                page.evaluate("window.scrollBy(0, 500)")
            elif direction.lower() == "up":
                page.evaluate("window.scrollBy(0, -500)")
            elif direction.lower() == "bottom":
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            else:
                return "Invalid direction. Use 'down', 'up', or 'bottom'"
            
            time.sleep(1)
            return f"Scrolled {direction}"
        except Exception as e:
            return f"Error scrolling: {str(e)}"
    
    async def _arun(self, direction: str) -> str:
        raise NotImplementedError

class PressKeyTool(BaseTool):
    name: str = "press_key"
    description: str = "Press a keyboard key. Common keys: Enter, Tab, Escape, ArrowDown, ArrowUp"
    
    def _run(self, key: str) -> str:
        try:
            page = browser_manager.get_page()
            page.keyboard.press(key)
            return f"Pressed key: {key}"
        except Exception as e:
            return f"Error pressing key: {str(e)}"
    
    async def _arun(self, key: str) -> str:
        raise NotImplementedError

# Tool Registry for easy configuration
class ToolRegistry:
    def __init__(self):
        self.tools = []
        self._register_default_tools()
    
    def _register_default_tools(self):
        """Register default browser automation tools"""
        self.tools = [
            NavigateTool(),
            ClickElementTool(),
            TypeTextTool(),
            ExtractElementsTool(),
            GetPageInfoTool(),
            WaitTool(),
            ScrollTool(),
            PressKeyTool()
        ]
    
    def add_tool(self, tool: BaseTool):
        """Add a custom tool to the registry"""
        self.tools.append(tool)
    
    def get_tools(self) -> List[BaseTool]:
        """Get all registered tools"""
        return self.tools

# Create the agent
def create_browser_agent():
    """Create and configure the browser automation agent"""
    
    # Initialize tool registry
    tool_registry = ToolRegistry()
    tools = tool_registry.get_tools()
    
    # Create prompt template
    prompt = PromptTemplate.from_template(
        """
You are a browser automation assistant. You help users interact with web pages by navigating, clicking, typing, and extracting information.

Available tools:
{tools}

Tool Names: {tool_names}

Previous conversation:
{history}

When given a task:
1. Break it down into steps if complex
2. Use appropriate tools in sequence
3. Verify actions succeeded before proceeding
4. Extract and report relevant information

Current task: {input}

Format for each step:
Thought: [your reasoning here]
Action: [tool name]
Action Input: [input for the tool]
Observation: [result of the action]

Repeat until the task is complete, then provide a final answer.

{agent_scratchpad}
"""
    )
    
    # Create memory
    memory = ConversationBufferMemory(
        memory_key="history",
        return_messages=False
    )
    
    # Create the agent
    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )
    
    # Create agent executor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        max_iterations=15,
        handle_parsing_errors=True
    )
    
    return agent_executor, tool_registry

# Main execution
def run_browser_task(task: str):
    """Execute a browser automation task"""
    try:
        # Start browser
        browser_manager.start()

        # Create agent
        agent_executor, _ = create_browser_agent()

        # Execute task
        result = agent_executor.invoke({"input": task})
        return result['output']

    except Exception as e:
        return f"Error executing task: {str(e)}"

    finally:
        # Keep browser open for inspection
        pass

# Simple example usage
if __name__ == "__main__":
    try:
        # Example 1: Simple step-by-step task
        task = """Navigate to https://www.saucedemo.com/. 
        
        Login using username 'standard_user' and password 'secret_sauce'.
        
        Add the 'Sauce Labs Bike Light' to the cart.
        
        Go to the cart and checkout.
        
        Enter shipping info with first name 'John', last name 'Doe', and postal code '12345'.
        
        Click continue and finish the order.
        
        Click on 'Back Home' to return to the homepage.
        
        click on the menu
        
        Click on 'Logout' to log out of the application.

        Finally, take a screenshot of the homepage and save it as 'final_homepage.png'.
        """

        print(f"Executing task: {task}\n")
        result = run_browser_task(task)
        print(f"\nResult: {result}")
        
        # Keep browser open for 5 seconds to see results
        time.sleep(5)
        
    finally:
        # Clean up
        browser_manager.stop()
        print("\nBrowser closed.")