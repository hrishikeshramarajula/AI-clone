#!/bin/bash

# Scout AI Clone - Development Server Launcher
# This script starts both frontend and backend servers

echo "🚀 Starting Scout AI Clone..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Backend server will not start."
    echo "   Install Python 3.10+ to enable backend functionality."
    BACKEND_AVAILABLE=false
else
    BACKEND_AVAILABLE=true
fi

# Check if Bun is installed, fallback to npm
if command -v bun &> /dev/null; then
    PACKAGE_MANAGER="bun"
elif command -v npm &> /dev/null; then
    PACKAGE_MANAGER="npm"
else
    echo "❌ Neither Bun nor npm is installed. Please install one to continue."
    exit 1
fi

echo "📦 Using $PACKAGE_MANAGER as package manager"
echo ""

# Function to kill background processes on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down servers..."
    kill $FRONTEND_PID $BACKEND_PID 2>/dev/null
    exit 0
}

trap cleanup EXIT INT TERM

# Start backend server if Python is available
if [ "$BACKEND_AVAILABLE" = true ]; then
    echo "🔧 Starting backend server..."
    cd server
    python3 server.py &
    BACKEND_PID=$!
    cd ..
    echo "✅ Backend server started (PID: $BACKEND_PID)"
    echo "   Available at: http://localhost:8000"
    echo ""
fi

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    $PACKAGE_MANAGER install
    echo ""
fi

# Start frontend server
echo "🎨 Starting frontend server..."
$PACKAGE_MANAGER run dev &
FRONTEND_PID=$!
echo "✅ Frontend server started (PID: $FRONTEND_PID)"
echo "   Available at: http://localhost:5173"
echo ""

echo "==========================================="
echo "✨ Scout AI Clone is running!"
echo ""
echo "🌐 Frontend: http://localhost:5173"
if [ "$BACKEND_AVAILABLE" = true ]; then
    echo "🔌 Backend:  http://localhost:8000"
    echo "📚 API Docs: http://localhost:8000/docs"
fi
echo ""
echo "Press Ctrl+C to stop all servers"
echo "==========================================="

# Wait for background processes
wait