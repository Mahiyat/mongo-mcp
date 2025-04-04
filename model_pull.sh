#!/bin/bash

# Define variables for the container name
CONTAINER_NAME="ollama-llm"

# Function to check if a command was successful
check_success() {
  if [ $? -ne 0 ]; then
    echo "Error: $1"
    exit 1
  fi
}

echo "Starting the model pulling in ollama-llm..."

# Pull the llama3.2 model
echo "Pulling the llama3.2 model..."
docker exec -it $CONTAINER_NAME ollama pull llama3.2
check_success "Failed to pull the llama3.2 model."

echo "Model pulling completed successfully!"
