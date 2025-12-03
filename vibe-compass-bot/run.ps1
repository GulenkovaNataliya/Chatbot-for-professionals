# PowerShell скрипт для запуска бота
# Запуск: щелкните правой кнопкой -> "Выполнить с помощью PowerShell"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Starting Vibe-Compass Bot" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Переход в директорию скрипта
Set-Location $PSScriptRoot

# Проверка Python
Write-Host "[1/5] Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = & python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "OK: $pythonVersion" -ForegroundColor Green
    } else {
        throw "Python not found"
    }
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH!" -ForegroundColor Red
    Write-Host "Please install Python from https://www.python.org/" -ForegroundColor Red
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

# Проверка .env
Write-Host "[2/5] Checking .env file..." -ForegroundColor Yellow
if (-Not (Test-Path ".env")) {
    Write-Host "ERROR: .env file not found!" -ForegroundColor Red
    Write-Host "Please create .env file with your TELEGRAM_BOT_TOKEN" -ForegroundColor Red
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "OK: .env file found" -ForegroundColor Green
Write-Host ""

# Проверка зависимостей
Write-Host "[3/5] Checking dependencies..." -ForegroundColor Yellow
$checkDeps = & python -c "import telegram" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "WARNING: python-telegram-bot not installed!" -ForegroundColor Yellow
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    & python -m pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
        Write-Host ""
        Read-Host "Press Enter to exit"
        exit 1
    }
}
Write-Host "OK: Dependencies installed" -ForegroundColor Green
Write-Host ""

# Проверка базы данных
Write-Host "[4/5] Checking database..." -ForegroundColor Yellow
if (-Not (Test-Path "vibe_compass.db")) {
    Write-Host "Initializing database..." -ForegroundColor Yellow
    & python database.py
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to initialize database" -ForegroundColor Red
        Write-Host ""
        Read-Host "Press Enter to exit"
        exit 1
    }
}
Write-Host "OK: Database ready" -ForegroundColor Green
Write-Host ""

# Запуск бота
Write-Host "[5/5] Starting bot..." -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop the bot" -ForegroundColor Cyan
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

& python bot.py

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "ERROR: Bot crashed with error code $LASTEXITCODE" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
}

Write-Host ""
Read-Host "Press Enter to exit"
