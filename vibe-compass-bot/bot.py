"""
Главный файл бота "Вайб-Компас Освобождения"
Запуск: python bot.py
"""
import sys
import os

# Настройка UTF-8 для Windows
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters
)
import logging

from config import TELEGRAM_BOT_TOKEN, START, QUESTION_1_EMOTION, QUESTION_2_PAIN, QUESTION_3_TIME, SHOW_OFFER, COMPLETE
from handlers import *
from database import init_db

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    """Главная функция запуска бота"""

    # Проверка токена
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == 'your_bot_token_here':
        logger.error("❌ ОШИБКА: Токен бота не установлен!")
        logger.error("Создайте файл .env и добавьте TELEGRAM_BOT_TOKEN=ваш_токен")
        return

    # Инициализация базы данных
    logger.info("Инициализация базы данных...")
    init_db()

    # Создание приложения
    logger.info("Создание приложения бота...")
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Определение ConversationHandler для основного сценария
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start_command),
            CallbackQueryHandler(start_quiz_callback, pattern='^start_quiz$')
        ],
        states={
            START: [
                CallbackQueryHandler(start_quiz_callback, pattern='^start_quiz$'),
                CallbackQueryHandler(remind_later_callback, pattern='^remind_later$')
            ],
            QUESTION_1_EMOTION: [
                CallbackQueryHandler(emotion_callback, pattern='^emotion_')
            ],
            QUESTION_2_PAIN: [
                CallbackQueryHandler(pain_callback, pattern='^pain_')
            ],
            QUESTION_3_TIME: [
                CallbackQueryHandler(time_callback, pattern='^time_')
            ],
            SHOW_OFFER: [
                CallbackQueryHandler(consultation_callback, pattern='^action_consultation$'),
                CallbackQueryHandler(pdf_callback, pattern='^action_pdf$'),
                CallbackQueryHandler(later_callback, pattern='^action_later$')
            ],
            COMPLETE: [
                CallbackQueryHandler(reminder_yes_callback, pattern='^reminder_yes$'),
                CallbackQueryHandler(reminder_no_callback, pattern='^reminder_no$'),
                CallbackQueryHandler(start_quiz_callback, pattern='^start_quiz$')
            ]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        name="main_conversation",
        persistent=False
    )

    # Регистрация обработчиков
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('stats', stats_command))

    # Запуск бота
    logger.info("✅ Бот запущен и готов к работе!")
    logger.info("Нажмите Ctrl+C для остановки")

    # Запуск polling
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n👋 Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")
        raise
