#!/bin/bash
# Скрипт для запуска бота на PythonAnywhere

echo "Starting Vibe-Compass Bot..."

# Переход в директорию проекта
cd ~/vibe-compass-bot

# Активация виртуального окружения
source venv/bin/activate

# Проверка .env файла
if [ ! -f .env ]; then
    echo "ERROR: .env file not found!"
    exit 1
fi

# Инициализация базы данных (если нужно)
python database.py

# Запуск бота
python bot.py
