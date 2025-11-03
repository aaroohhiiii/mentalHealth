#!/bin/bash
# 
# Development Server Startup Script
# Starts backend with auto-reload capability
#

echo "=================================="
echo "🚀 Starting MindEase Backend (Dev Mode)"
echo "=================================="

cd "$(dirname "$0")"

# Kill any existing server
echo "🧹 Cleaning up existing processes..."
lsof -ti:8000 | xargs kill -9 2>/dev/null
pkill -9 -f "uvicorn app:app" 2>/dev/null
pkill -9 -f "dev_server.py" 2>/dev/null

sleep 2

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if watchdog is installed
if ! python -c "import watchdog" 2>/dev/null; then
    echo "📦 Installing watchdog..."
    pip install watchdog
fi

# Start dev server with auto-reload
echo ""
echo "✅ Starting server with auto-reload..."
echo "📂 Watching: backend/*.py files"
echo "🌐 URL: http://127.0.0.1:8000"
echo ""
echo "Press Ctrl+C to stop"
echo "=================================="
echo ""

python dev_server.py
