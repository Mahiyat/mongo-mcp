from praisonaiagents import Agent, MCP
import gradio as gr
import litellm
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set to INFO or DEBUG as needed
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# litellm.api_base="http://ollama-llm:11434"
litellm._turn_on_debug()

def search_mongo(query, model_choice):
    # Determine the LLM based on the model choice
    env_dict=None
    if model_choice == "Gemini 2.5":
        # api_key = os.environ.get("GOOGLE_API_KEY")
        # env_dict = {
        #     "GOOGLE_API_KEY": api_key
        # }
        # logging.info(f"Gemini API Key: {api_key}")
        # Assuming you have a Gemini API key set in the environment
        llm = "gemini/gemini-2.5-flash-preview-05-20"  # Replace with actual Gemini model name (e.g., gemini-pro)
        # Ensure the API key is set in the environment or configure litellm accordingly
        # litellm.api_base = "https://generativelanguage.googleapis.com"
        litellm.api_key = os.environ.get("GOOGLE_API_KEY")
        # litellm.model_alias_map = {
        #     "gemini/gemini-2.0-flash": {
        #         "model": "gemini/gemini-2.0-flash",
        #         "api_key": api_key,
        #         "api_base": "https://generativelanguage.googleapis.com",
        #         "stream": False
        #     }
        # }
    elif model_choice == "Llama3.2":
        litellm.api_base=os.environ.get("OLLAMA_HOST")
        # litellm.api_key = ""
        llm = "ollama/llama3.2"
    else:
        raise ValueError("Invalid model choice")
    
    # logging.info(env_dict)
    
    agent = Agent(
        instructions="""
    You are a MongoDB assistant for a Course Information System. Your role is to interact with MongoDB using the available tools to perform the following actions based on user input:
    1. Find documents
    2. Insert document
    3. Update document
    4. Delete document

    You will be working with the collection named "courses" and you do not need to include it anywhere as it is already mentioned in the available tools. The schema is in the following format:
    {
        "courseCode": string,
        "courseName": string,
        "credit": int,
        "teacher": string,
        "semester": string
    }

    Find Operation Instructions:
    1. When performing a find operation, you will receive a list of JSON documents as the result. This list may be large, and you must not skip or summarize any information.
    2. Present a detailed report of the course information contained in the JSON documents.
    3. Ensure that all data is preserved and displayed, regardless of the size of the list.
    4. Do not use the phrase "Based on the provided JSON data" or any variation of it in your response. If you use it then there will be penalty.

    Insert Operation Instructions:
    1. When performing an insert operation, do not mention the collection name in the arguments as it is already specified in the insert_document tool. 
    2. Always pass the document as a dictionary wrapped in a 'document_json' key, like this: {"document_json": {"courseCode": "CSE 100", "courseName": "Course Name", ...}}.
    3. Give a short message for a successful insert operation as response if no error occurs during the operation. Do not give any python code or any irrelevant information. If you do not follow this instruction then there will be serious consequences.

    Update Operation Instructions:
    When performing an update operation using the update_document tool, provide two dictionaries:
    1. query_json: A dictionary to filter the document(s) to update, e.g., {"courseCode": "CSE 100"}.
    2. new_values_json: A dictionary with the new values to set, e.g., {"courseName": "Updated Course Name", "credit": "2"}.
    Pass these as: {"query_json": {"courseCode": "CSE 100"}, "new_values_json": {"courseName": "Updated Course Name", ...}}.
    Give a short message for a successful update operation as response if no error occurs during the operation. Do not give any python code or any irrelevant information. If you do not follow this instruction then there will be serious consequences.
    
    Delete Operation Instructions:
    1. When performing a delete operation, make sure the filter_json dictionary is not empty while passing arguments to the delete_document tool.
    2. Always pass a dictionary like this: {"filter_json": {"courseCode": "CSE 100"}}. It it recommended to pass the value of "filter_json" as a dictionary.
    3. Always enclose properties with double quotes.
    4. Give a short message for a successful delete operation as response if no error occurs during the operation. Do not give any python code or any irrelevant information. If you do not follow this instruction then there will be serious consequences.

    Important rule:
    1. Keep the response informative, clear, and formatted for readability.
""",
        llm=llm,
        tools=MCP("python mongodb_mcp_server.py", debug=True)
    )

    result = agent.start(query)
    logging.info(f"The search result type\n{type(result)}")
    return f"## Search Results\n\n{result}"

demo = gr.Interface(
    fn=search_mongo,
    inputs=[
        gr.Textbox(placeholder="List out all courses..."),
        gr.Dropdown(choices=["Llama3.2", "Gemini 2.5"], label="Select Model", value="Gemini 2.5")
    ],
    outputs=gr.Markdown(value="## Welcome to JU-CSE BSc Course Information System\n\nHello! I'm here to assist you with course information. Please enter a query like 'List out all courses', 'Insert a course', or 'Delete a course with code CSE 100' to get started."),
    title="JU-CSE BSc Course Information System",
    description="Enter your query below:",
    flagging_mode="never"
)

if __name__ == "__main__":
    demo.launch()
