#!/bin/bash

# Mental Health AI - Server Startup Script
# This script ensures clean virtual environment and starts the server

cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

# Set Python path to use ONLY venv packages
export PYTHONPATH="$(pwd):$(pwd)/venv/lib/python3.10/site-packages"

# Prevent system TensorFlow from interfering
export PYTHONNOUSERSITE=1

# Start the server
echo "🚀 Starting Mental Health AI Server..."
echo "   Virtual environment: $(which python)"
echo "   Server will be available at: http://localhost:8000"
echo "   API docs at: http://localhost:8000/docs"
echo ""

uvicorn app:app --reload --host 0.0.0.0 --port 8000
