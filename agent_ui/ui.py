from praisonaiagents import Agent, MCP
import gradio as gr
import litellm
import os

# litellm.api_base="http://ollama-llm:11434"
litellm.api_base=os.environ.get("OLLAMA_HOST")

def search_mongo(query):
    agent = Agent(
        instructions="""
    You are a MongoDB assistant for a Course Information System. Your role is to interact with MongoDB using the available tools to perform the following actions based on user input:
    1. Find documents
    2. Insert documents
    3. Delete documents
    When performing an insert operation, do not mention the collection name in the arguments as it is already specified in the insert_document tool. Always pass the document as a dictionary wrapped in a 'document_json' key, like this: {"document_json": {"courseCode": "CSE 100", "courseName": "Course Name", ...}}.
    When performing a find operation, you will receive a list of JSON documents as the result. This list may be large, and you must not skip or summarize any information.
    Your task is:
    1. Present a detailed report of the course information contained in the JSON documents.
    2. Ensure that all data is preserved and displayed, regardless of the size of the list.
    3. Do not let the user know you are giving the response based on the JSON data.
    Important rules:
    1. Do not use the phrase "Based on the provided JSON data" or any variation of it in your response.
    2. Keep the response informative, clear, and formatted for readability.
    3. In case of performing an insert or a delete operation, respond with an assurance message that the operation is being performed successfully if no error is thrown. Do not mention the value of the _id. Also do not give any python code in the response.
""",
        llm="ollama/llama3.2",
        tools=MCP("python mongodb_mcp_server.py", debug=True)
    )

    result = agent.start(query)
    return f"## Search Results\n\n{result}"

demo = gr.Interface(
    fn=search_mongo,
    inputs=gr.Textbox(placeholder="List out all courses..."),
    outputs=gr.Markdown(),
    title="JU-CSE BSc Course Information System",
    description="Enter your query below:"
)

if __name__ == "__main__":
    demo.launch()
