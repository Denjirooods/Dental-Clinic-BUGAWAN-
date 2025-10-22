@echo off
title Macvil Dental Clinic - Inventory Management System
echo.
echo ========================================
echo   Macvil Dental Clinic
echo   Inventory Management System
echo ========================================
echo.
echo Starting the system...
echo.
echo Please wait while the system initializes...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.7 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

REM Check if requirements are installed
echo Checking dependencies...
pip install -r requirements.txt --quiet

REM Start the application
echo.
echo Starting Flask application...
echo.
echo The system will be available at: http://localhost:5000
echo.
echo Default login credentials:
echo Username: admin
echo Password: admin123
echo.
echo Press Ctrl+C to stop the system
echo.
echo ========================================
echo.

python app.py

echo.
echo System stopped.
pause



