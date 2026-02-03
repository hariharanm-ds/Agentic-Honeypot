@echo off
REM Agentic Honeypot - Quick Start Script
REM This script starts the API server and opens the frontend

echo.
echo ========================================
echo Agentic Honeypot System - Startup
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python and try again
    exit /b 1
)

echo [1/3] Checking dependencies...
python -m pip show flask >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
)

echo [OK] Dependencies ready
echo.

echo [2/3] Starting API server...
echo API will run on http://localhost:5000
echo Press Ctrl+C to stop
echo.

start /B python -m src.api

REM Wait for API to start
timeout /t 3 /nobreak

echo [3/3] Opening Web Interface...
timeout /t 1 /nobreak

REM Try to open in default browser
start index.html

echo.
echo ========================================
echo Web Interface: http://localhost:5000
echo Frontend: Open index.html in browser
echo API Status: http://localhost:5000/health
echo ========================================
echo.
pause
