@echo off
REM PDF Q&A Assistant - Run Script

echo.
echo ========================================
echo PDF Q&A Assistant
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Virtual environment not found!
    echo Please run install.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the application
echo Starting PDF Q&A Assistant...
echo.
echo Server will be available at: http://localhost:8000
echo.
echo Press Ctrl+C to stop the server.
echo.

python main.py

pause
