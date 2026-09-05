@echo off
title Career Intelligence Platform Launcher
echo =========================================
echo  Career Intelligence Platform Launcher
echo =========================================
echo.

set ROOT_DIR=%~dp0

echo [1/2] Starting Backend Server (FastAPI)...
start "Career Intelligence - Backend" cmd /k "cd /d %ROOT_DIR%backend && .\venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000"

echo [2/2] Starting Frontend Server (Vite)...
start "Career Intelligence - Frontend" cmd /k "cd /d %ROOT_DIR%frontend && npm run dev"

echo.
echo =========================================
echo Both services are launching!
echo Frontend:  http://localhost:5173
echo Backend:   http://localhost:8000
echo API Docs:  http://localhost:8000/docs
echo Demo User: demo@careerai.com / demo123
echo =========================================
pause
