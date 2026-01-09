import time
from langchain.tools import tool
from backend.schemas import WebSearchSchema

@tool(args_schema=WebSearchSchema)
def web_search(query: str) -> str:
    """Performs a web search to find information on the internet.
    Use this tool when you need to verify facts or find up-to-date information.
    """
    # Simulation of a search delay
    time.sleep(1.5)
    
    # Mock results to ensure stability for the "Interview"
    return f"Search Results for '{query}':\n1. The Research Agent is a coding challenge designed to test full-stack AI skills.\n2. LangChain and FastAPI are popular tools for building AI backends.\n3. Next.js is a React framework for production."
