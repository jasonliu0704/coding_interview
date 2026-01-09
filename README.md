# Research Agent Coding Challenge

This repository contains the solution for the "Research Agent" practical challenge. It consists of a FastAPI backend and a Next.js frontend.

## Features Implemented

1.  **Backend (FastAPI + LangChain)**:
    *   **Schema Fix**: `WebSearchSchema` correctly defines the `query` field with a description so the LLM knows how to use it.
    *   **Streaming**: The agent uses `astream_events` to stream both "thoughts" (tool usage status) and the final "answer" in real-time.
    *   **Fake Web Search**: A simulated tool that returns mock results for stability.

2.  **Frontend (Next.js + React)**:
    *   **Real-time Streaming**: A custom `useChat` hook handles the `ndjson` stream.
    *   **Thought Trace**: A UI component that displays "Searching..." animations while the backend is processing tool calls, separate from the final text response.
    *   **Modern Design**: Styled with vanilla CSS variables, glassmorphism touches, and Framer Motion animations.

## Setup Instructions

### Backend

1.  Navigate to the `backend` directory:
    ```bash
    cd backend
    ```
2.  Create a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Set your OpenAI API Key:
    ```bash
    export OPENAI_API_KEY="sk-..."
    ```
5.  Run the server:
    ```bash
    uvicorn main:app --reload
    ```
    The backend runs on `http://localhost:8000`.

### Frontend

1.  Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Run the development server:
    ```bash
    npm run dev
    ```
    The frontend runs on `http://localhost:3000`.

## Architecture Decisions & "Context Awareness"

-   **Streaming Protocol**: We use Newline Delimited JSON (ndjson) to send multiple typed events (`thought`, `answer`) over a single HTTP response stream. This allows the frontend to easily distinguish between intermediate tool activity and the final answer.
-   **Agent Memory**: currently, the conversation state is held in the React client's state and passed (simulated) or just single-turn in this simple demo.
    *   **Production Note**: For a real-world "Research Agent," we would implement **Persistent Memory**.
    *   **Implementation**: We would use **Redis** (for short-term caching of message history) or **PostgreSQL** (with `pgvector` for semantic search if we need to recall older conversations).
    *   **LangChain Integration**: We would wrap the `AgentExecutor` with `RunnableWithMessageHistory` backed by a `RedisChatMessageHistory` or `PostgresChatMessageHistory` class.

## Error Handling

-   The frontend's stream reader is wrapped in a `try/catch` block to handle potential JSON parsing errors if a chunk is split unexpectedly or if the network fails.
-   The backend also catches exceptions during the agent run and yields an error event to the client.
# coding_interview
