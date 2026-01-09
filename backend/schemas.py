from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str

class WebSearchSchema(BaseModel):
    # BUG: Missing description for 'query' causing potential LLM confusion
    query: str
