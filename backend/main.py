from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.agent import run_agent
from backend.schemas import ChatRequest
import logging

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
    # BUG: This waits for the entire agent execution (including 3s sleep) before returning anything
    response_text = run_agent(request.message)
    return {"message": response_text}

@app.get("/health")
def health_check():
    return {"status": "ok"}
