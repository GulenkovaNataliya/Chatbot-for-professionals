@echo off
echo ========================================
echo Installing Vibe-Compass Bot Dependencies
echo ========================================
echo.

cd /d "%~dp0"

echo Step 1: Checking Python...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)
echo.

echo Step 2: Installing dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.

echo Step 3: Initializing database...
python database.py
if %errorlevel% neq 0 (
    echo ERROR: Failed to initialize database
    pause
    exit /b 1
)
echo.

echo ========================================
echo Installation completed successfully!
echo ========================================
echo.
echo You can now run the bot with: python bot.py
echo.
pause
