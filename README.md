# JU-CSE BSc Course Information System

A comprehensive course information management system built with MongoDB, AI agents, and a user-friendly web interface. This system allows users to interact with course data using natural language queries powered by Large Language Models (LLMs).

## Features

- **Natural Language Interface**: Query course information using plain English
- **Multiple LLM Support**: Choose between Gemini 2.5 (cloud) and Llama 3.2 (local)
- **Complete CRUD Operations**: Create, Read, Update, and Delete course records
- **MongoDB Integration**: Robust data storage with MongoDB
- **Web UI**: Gradio-based web interface for easy interaction
- **Containerized**: Fully containerized with Docker Compose
- **MCP Integration**: Uses Model Context Protocol for seamless tool integration

N.B. Ollama integration is not working for now.

## Course Data Schema

```json
{
  "courseCode": "string",
  "courseName": "string", 
  "credit": "int",
  "teacher": "string",
  "semester": "string"
}
```

## Architecture

The system consists of several containerized services:

- **MongoDB**: Database for storing course information
- **Ollama**: Local LLM service running Llama 3.2
- **Agent**: Core AI agent with MongoDB MCP server
- **Agent UI**: Gradio web interface for user interaction

## Prerequisites

- Docker and Docker Compose
- NVIDIA GPU (for Ollama container)
- Google API Key (for Gemini 2.5 support)

## Quick Start

### 1. Clone and Setup

```bash
git clone git@github.com:Mahiyat/mongo-mcp.git
cd mongo-mcp
```

### 2. Environment Configuration

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Add your Google API key to the `.env` file:

```bash
GOOGLE_API_KEY=your_google_api_key_here
```

### 3. Start Services

```bash
# Start all services
docker-compose up -d --build

# Wait for services to be ready
docker-compose logs -f
```

### 4. Pull Ollama Model

```bash
# Make the script executable
chmod +x model_pull.sh

# Pull the Llama 3.2 model
./model_pull.sh
```

### 5. Access the Application

Open your browser and navigate to:
```
http://localhost:7860
```

## Usage Examples

### Finding Courses
- "List out all the courses."
- "List out the courses having 3 credit."
- "List out the courses taught by Dr. Smith."
- "List out all the courses of 1st Year 2nd Semester."

### Adding Courses
- "Insert a course with the following information:
    courseCode: CSE-101,
    courseName: MathematicsI,
    credit: 3,
    teacher: Dr. Smith,
    semester: 1st Year 1st Semester"

### Updating Courses
- "Update course CSE-101 to have 4 credits."
- "Change the teacher of CSE-202 to Dr. Williams."

### Deleting Courses
- "Delete the course with code CSE-101."
- "Delete the course named Electrical Circuits."

## API Endpoints

### MongoDB MCP Server Tools

The system provides the following tools through the MCP server:

- `find_documents(filter_json, limit)`: Search for courses
- `insert_document(document_json)`: Add new courses
- `update_document(query_json, new_values_json)`: Update existing courses
- `delete_document(filter_json)`: Remove courses

## Development

### Project Structure

```
.
├── agent/                    # Core agent service
│   ├── Dockerfile.agent
│   ├── mongodb_mcp_server.py # MCP server implementation
│   ├── requirement.txt
│   └── run_agent.py         # Agent runner
├── agent_ui/                # Web interface
│   ├── Dockerfile
│   ├── requirement.txt
│   └── ui.py               # Gradio web UI
├── docker-compose.yml      # Service orchestration
├── Dockerfile.ollama       # Ollama LLM service
├── model_pull.sh          # Model installation script
└── .env.example           # Environment template
```

## Configuration

### Environment Variables

- `GOOGLE_API_KEY`: Google API key for Gemini 2.5
- `OLLAMA_HOST`: Ollama service endpoint
- `MONGO_URI`: MongoDB connection string
- `MONGO_DB`: MongoDB database name

### Model Configuration

The system supports two LLM options:

1. **Llama 3.2 (Local)**
   - Runs locally via Ollama
   - No API key required
   - Requires GPU for optimal performance

2. **Gemini 2.5 (Cloud)**
   - Requires Google API key
   - Better performance for complex queries
   - Internet connection required

## Troubleshooting

### Common Issues

1. **Ollama model not found**
   ```bash
   ./model_pull.sh
   ```

2. **MongoDB connection failed**
   ```bash
   docker-compose restart mongo
   ```

3. **GPU not available**
   - Remove GPU configuration from docker-compose.yml
   - Models will run on CPU (slower)

4. **Port conflicts**
   - Change port mappings in docker-compose.yml
   - Default ports: 7860 (UI), 11434 (Ollama), 27017 (MongoDB)

### Logs

```bash
# View all service logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f agent_ui
docker-compose logs -f ollama-llm
docker-compose logs -f mongo
```
## Acknowledgments

- PraisonAI Agents for the agent framework
- MongoDB for database services
- Ollama for local LLM inference
- Gradio for the web interface
- Google for Gemini API access