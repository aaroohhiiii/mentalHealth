#!/bin/bash
# Helper script to restart the backend server
# Usage: ./restart_server.sh

echo "🔄 Restarting backend server..."

# Kill any existing server on port 8000
lsof -ti:8000 | xargs kill -9 2>/dev/null
pkill -9 -f "uvicorn app:app" 2>/dev/null
sleep 2

# Navigate to backend directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Start server using venv python directly (avoids mutex errors)
echo "Starting server..."
nohup "$SCRIPT_DIR/venv/bin/python" -m uvicorn app:app --host 127.0.0.1 --port 8000 > server.log 2>&1 &

sleep 3

# Check if server started
if curl -s http://127.0.0.1:8000/ > /dev/null 2>&1; then
    echo "✅ Server restarted successfully on http://127.0.0.1:8000"
else
    echo "⚠️  Server may still be starting... check server.log"
    tail -10 server.log
fi
