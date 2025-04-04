from praisonaiagents import Agent, MCP
import litellm
import os

# litellm.api_base="http://ollama-llm:11434"
litellm.api_base=os.environ.get("OLLAMA_HOST")
litellm._turn_on_debug()

agent = Agent(
    instructions="""You are a MongoDB assistant. You can find, insert, and delete documents based on user input using the available tools.""",
    llm="ollama/llama3.2",
    tools=MCP("python mongodb_mcp_server.py", debug=True)
)

agent.start("Insert a document in the MongoDB collection where the name is Software Engineering, description is Intro to SE.")
