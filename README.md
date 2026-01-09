# The Practical Challenge: "The Research Agent" (60 Minutes)

This repository contains a basic FastAPI backend and a React (Next.js) frontend. 

**The Goal:** The agent successfully uses a "web_search" tool, but the implementation is buggy and provides a poor user experience. Your job is to fix the schema issues and upgrade the system to support real-time streaming of "thoughts" and answers.

## 1. Python Backend Task (25 Minutes)

**Scenario:** The agent uses a `web_search` tool. However, it often fails to use it correctly or crashes because of a schema definition issue. Additionally, the user has to wait ~3 seconds staring at a spinner before seeing any text.

**The Tasks:**
1.  **Fix the Bug:** The Pydantic schema (`backend/schemas.py`) for the web_search tool has a type/description mismatch. Fix it so the LLM correctly parses the "query" argument.
2.  **Streaming Upgrade:** Refactor the endpoint (`backend/main.py` and `backend/agent.py`) to use `astream_events` (or a similar LangChain streaming method). 
    *   The backend should yield JSON events for "thoughts" (e.g. `{"type": "thought", "status": "searching", ...}`) when the tool starts/ends.
    *   It should yield "answer" events (e.g. `{"type": "answer", "content": "The result is..."}`) as the token stream arrives.

## 2. React Frontend Task (20 Minutes)

**Scenario:** The UI currently just shows a loading spinner until the full text arrives (blocking HTTP request).

**The Tasks:**
1.  **Handle Streaming:** Modify `frontend/app/hooks/useChat.ts` to read a stream of newline-delimited JSON objects (NDJSON) instead of awaiting the full response.
2.  **Visual Feedback:** Implement the `ThoughtTrace` component (`frontend/app/components/ThoughtTrace.tsx`).
    *   It should display a "Searching..." status (with a small animation) when a "thought" event of type `searching` is received.
    *   It should disappear or show a checkmark when the search is done.

## 3. Evaluation Criteria (15 Minutes Code Walkthrough)

*   **Error Resilience:** Does the frontend crash if a JSON chunk is malformed?
*   **Context Awareness:** (Bonus/Discussion) How would you persist this conversation? Redis? Postgres?
*   **Streaming Mastery:** Did you correctly use `ReadableStream` and `TextDecoder`?

## Setup

### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Create .env with OPENAI_API_KEY=...
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Good luck!
