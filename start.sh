#!/bin/bash

# Agentic Honeypot - Quick Start Script
# This script starts the API server and opens the frontend

echo ""
echo "========================================"
echo "Agentic Honeypot System - Startup"
echo "========================================"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    exit 1
fi

echo "[1/3] Checking dependencies..."
if ! python3 -c "import flask" 2>/dev/null; then
    echo "Installing required packages..."
    pip install -r requirements.txt
fi

echo "[OK] Dependencies ready"
echo ""

echo "[2/3] Starting API server..."
echo "API will run on http://localhost:5000"
echo "Press Ctrl+C to stop"
echo ""

python3 -m src.api &
API_PID=$!

# Wait for API to start
sleep 3

echo "[3/3] Opening Web Interface..."

# Try to open in default browser
if command -v open &> /dev/null; then
    open index.html
elif command -v xdg-open &> /dev/null; then
    xdg-open index.html
fi

echo ""
echo "========================================"
echo "Web Interface: http://localhost:5000"
echo "Frontend: Open index.html in browser"
echo "API Status: http://localhost:5000/health"
echo "========================================"
echo ""
echo "Press Enter to continue..."
read

# Cleanup on exit
kill $API_PID 2>/dev/null
