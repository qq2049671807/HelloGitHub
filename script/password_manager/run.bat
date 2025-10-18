@echo off
REM Password Manager Launcher Script for Windows

cd /d "%~dp0"

echo Checking dependencies...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH!
    echo Please install Python 3.7 or higher from https://www.python.org/
    pause
    exit /b 1
)

REM Check if dependencies are installed
python -c "import PyQt5; import cryptography" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo Failed to install dependencies!
        pause
        exit /b 1
    )
)

echo Starting Password Manager...
python password_manager.py

pause
