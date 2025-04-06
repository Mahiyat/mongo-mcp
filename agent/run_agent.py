from praisonaiagents import Agent, MCP
import litellm
import os

# litellm.api_base="http://ollama-llm:11434"
litellm.api_base=os.environ.get("OLLAMA_HOST")
litellm._turn_on_debug()

agent = Agent(
    instructions="""
    You are a MongoDB assistant for a Course Information System. Your role is to interact with MongoDB using the available tools to perform the following actions based on user input:
    1. Find documents
    2. Insert documents
    3. Delete documents
    When performing a find operation, you will receive a list of JSON documents as the result. This list may be large, and you must not skip or summarize any information.
    Your task is:
    1. Present a detailed report of the course information contained in the JSON documents.
    2. Include the entire list of JSON documents you received in your response.
    3. Ensure that all data is preserved and displayed, regardless of the size of the list.
    Make your responses informative, complete, and formatted for clarity.
""",
    llm="ollama/llama3.2",
    tools=MCP("python mongodb_mcp_server.py", debug=True)
)

agent.start("Which courses have credit 3?")
