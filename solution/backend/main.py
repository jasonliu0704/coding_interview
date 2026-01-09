from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from backend.agent import run_agent
from backend.schemas import ChatRequest
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    async def event_generator():
        try:
            async for event in run_agent(request.message):
                event_type = event.get("event")
                
                # Task 1.2: Yield "thought" events
                if event_type == "on_tool_start":
                    # Capture tool usage
                    tool_name = event["name"]
                    inputs = event["data"].get("input")
                    query = inputs.get("query") if inputs else "..."
                    
                    if tool_name == "web_search":
                        payload = {
                            "type": "thought",
                            "status": "searching",
                            "content": f"Searching the web for: {query}"
                        }
                        yield json.dumps(payload) + "\n"
                        
                elif event_type == "on_tool_end":
                    # Tool finished
                    payload = {
                        "type": "thought",
                        "status": "done",
                        "content": "Finished searching."
                    }
                    yield json.dumps(payload) + "\n"
                    
                elif event_type == "on_chat_model_stream":
                    # Capture final response tokens
                    chunk = event["data"]["chunk"]
                    if hasattr(chunk, "content") and chunk.content:
                        payload = {
                            "type": "answer",
                            "content": chunk.content
                        }
                        yield json.dumps(payload) + "\n"
                        
        except Exception as e:
            logger.error(f"Error during streaming: {e}")
            yield json.dumps({"type": "error", "content": str(e)}) + "\n"

    return StreamingResponse(event_generator(), media_type="application/x-ndjson")

@app.get("/health")
def health_check():
    return {"status": "ok"}
