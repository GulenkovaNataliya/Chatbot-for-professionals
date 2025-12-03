@echo off
echo ========================================
echo Starting Vibe-Compass Bot
echo ========================================
echo.

cd /d "%~dp0"

echo Checking if .env file exists...
if not exist .env (
    echo ERROR: .env file not found!
    echo Please create .env file with your TELEGRAM_BOT_TOKEN
    pause
    exit /b 1
)
echo.

echo Starting bot...
python bot.py

pause
