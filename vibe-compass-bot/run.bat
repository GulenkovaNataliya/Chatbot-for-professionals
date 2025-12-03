@echo off
chcp 65001 >nul
SET PYTHONIOENCODING=utf-8
echo ========================================
echo Starting Vibe-Compass Bot
echo ========================================
echo.

cd /d "%~dp0"

REM Определяем путь к Python
SET PYTHON_PATH=%LOCALAPPDATA%\Programs\Python\Python314\python.exe

echo [1/4] Checking Python installation...
if exist "%PYTHON_PATH%" (
    "%PYTHON_PATH%" --version
    echo.
) else (
    echo WARNING: Python 3.14 not found in standard location
    echo Trying system Python...
    python --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo ERROR: Python is not installed!
        echo Please install Python from https://www.python.org/
        pause
        exit /b 1
    )
    SET PYTHON_PATH=python
    python --version
    echo.
)

echo [2/4] Checking if .env file exists...
if not exist .env (
    echo ERROR: .env file not found!
    echo Please create .env file with your TELEGRAM_BOT_TOKEN
    pause
    exit /b 1
)
echo OK: .env file found
echo.

echo [3/4] Checking dependencies...
"%PYTHON_PATH%" -c "import telegram" >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: python-telegram-bot not installed!
    echo Installing dependencies...
    "%PYTHON_PATH%" -m pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)
echo OK: Dependencies installed
echo.

echo [4/4] Starting bot...
echo Press Ctrl+C to stop the bot
echo.
"%PYTHON_PATH%" bot.py

if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo ERROR: Bot crashed with error code %errorlevel%
    echo ========================================
)

pause
