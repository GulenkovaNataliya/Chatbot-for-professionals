"""
Клавиатуры для бота
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_start_keyboard():
    """Клавиатура для начального экрана"""
    keyboard = [
        [InlineKeyboardButton("✨ Да, поехали!", callback_data='start_quiz')],
        [InlineKeyboardButton("⏰ Позже...", callback_data='remind_later')]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_emotion_keyboard():
    """Клавиатура для вопроса об эмоциях"""
    keyboard = [
        [InlineKeyboardButton("🍋 Выжатый как лимон", callback_data='emotion_tired')],
        [InlineKeyboardButton("😤 Раздраженный, потому что не сделал главное", callback_data='emotion_annoyed')],
        [InlineKeyboardButton("🤯 Запутавшийся, не понимаю, куда ушло время", callback_data='emotion_confused')]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_pain_point_keyboard():
    """Клавиатура для выбора главной проблемы"""
    keyboard = [
        [InlineKeyboardButton("💬 Постоянно отвечаю на одни и те же вопросы", callback_data='pain_messages')],
        [InlineKeyboardButton("📊 Свожу данные из 10 таблиц в одну", callback_data='pain_data')],
        [InlineKeyboardButton("👨‍🍼 Напоминаю команде о дедлайнах", callback_data='pain_deadlines')],
        [InlineKeyboardButton("📄 Вручную формирую счета и документы", callback_data='pain_documents')],
        [InlineKeyboardButton("🔄 Копирую информацию из системы в систему", callback_data='pain_copying')]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_time_keyboard():
    """Клавиатура для оценки времени"""
    keyboard = [
        [InlineKeyboardButton("Меньше 5 часов", callback_data='time_low')],
        [InlineKeyboardButton("5-10 часов", callback_data='time_medium')],
        [InlineKeyboardButton("Больше 10 часов (спасите!)", callback_data='time_high')]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_offer_keyboard():
    """Клавиатура для предложения консультации"""
    keyboard = [
        [InlineKeyboardButton("✅ Да, хочу на стратегическую сессию!", callback_data='action_consultation')],
        [InlineKeyboardButton("📥 Скачать PDF-план '5 идей для вайбкодинга'", callback_data='action_pdf')],
        [InlineKeyboardButton("⏰ Вернуться позже", callback_data='action_later')]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_reminder_keyboard():
    """Клавиатура для напоминания"""
    keyboard = [
        [InlineKeyboardButton("✅ Да, напомни завтра", callback_data='reminder_yes')],
        [InlineKeyboardButton("❌ Нет, спасибо", callback_data='reminder_no')]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_back_to_start_keyboard():
    """Кнопка возврата к началу"""
    keyboard = [
        [InlineKeyboardButton("🔄 Начать заново", callback_data='start_quiz')]
    ]
    return InlineKeyboardMarkup(keyboard)
