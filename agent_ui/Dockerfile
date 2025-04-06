FROM python:3.11-slim

WORKDIR /agent

COPY agent_ui/requirement.txt .

RUN pip install --no-cache-dir -r requirement.txt

COPY agent_ui/ui.py .

COPY agent/mongodb_mcp_server.py .

EXPOSE 7860
# You can switch to Ollama by adding the ollama client if needed

CMD ["python", "ui.py"]
