from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str

class WebSearchSchema(BaseModel):
    """Schema for the web search tool."""
    # Task 1.1 Fix: Explicitly define query with description so LLM understands it
    query: str = Field(description="The search query to enter into the search engine.")
