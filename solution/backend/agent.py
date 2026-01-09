from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from backend.tools import web_search
import os

def get_agent_executor():
    # Helper to create the agent.
    # Note: Ensure OPENAI_API_KEY is set in your environment variables.
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, streaming=True)
    
    tools = [web_search]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful and precise research assistant."),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    agent = create_openai_tools_agent(llm, tools, prompt)
    
    # verbose=True helps with debugging logs
    executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return executor

async def run_agent(message: str):
    """
    Runs the agent and yields events from astream_events.
    """
    executor = get_agent_executor()
    
    # Task 1.2: Refactor to use astream_events
    async for event in executor.astream_events(
        {"input": message},
        version="v1"
    ):
        yield event
