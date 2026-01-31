@echo off
echo ==========================================
echo        Starting LocalRAG Project
echo ==========================================

REM Activate virtual environment
call venv\Scripts\activate

echo.
echo [1] Starting backend server...
start cmd /k "cd backend && uvicorn main:app --reload"

echo.
echo [2] Starting frontend server...
start cmd /k "cd frontend && python -m http.server 5500"

echo.
echo Both servers are now running.
echo Frontend:  http://localhost:5500
echo Backend:   http://127.0.0.1:8000
echo.
pause
