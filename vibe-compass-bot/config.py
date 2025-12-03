"""
Конфигурация бота
"""
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# CRM
AMOCRM_TOKEN = os.getenv('AMOCRM_TOKEN')
AMOCRM_DOMAIN = os.getenv('AMOCRM_DOMAIN')

# Database
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///vibe_compass.db')

# States для ConversationHandler
(
    START,
    QUESTION_1_EMOTION,
    QUESTION_2_PAIN,
    QUESTION_3_TIME,
    SHOW_INSIGHT,
    SHOW_OFFER,
    COMPLETE
) = range(7)

# Callback data prefixes
CALLBACK_PREFIX = {
    'emotion': 'emotion_',
    'pain': 'pain_',
    'time': 'time_',
    'action': 'action_'
}
