"""
Обработчики команд и кнопок бота
"""
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
import logging

from config import *
from messages import *
from keyboards import *
from database import *

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# ==================== КОМАНДЫ ====================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user = update.effective_user
    logger.info(f"Пользователь {user.first_name} ({user.id}) запустил бота")

    # Создаем или получаем пользователя в БД
    get_or_create_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name
    )

    await update.message.reply_text(
        START_MESSAGE,
        reply_markup=get_start_keyboard()
    )

    return START


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    help_text = """
🤖 **Вайб-Компас Освобождения**

Этот бот поможет тебе:
• Найти главный источник рутины в твоем бизнесе
• Получить персонализированный план автоматизации
• Связаться с экспертом для реализации

**Команды:**
/start - Начать диагностику
/stats - Статистика бота (только для админов)
/help - Эта справка

Просто следуй инструкциям бота!
    """
    await update.message.reply_text(help_text)


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Статистика бота (для админов)"""
    stats = get_statistics()

    stats_text = f"""
📊 **Статистика бота**

👥 Всего пользователей: {stats['total_users']}
✅ Завершили тест: {stats['completed']}
📈 Конверсия: {stats['completion_rate']:.1f}%

**Популярные проблемы:**
💬 Ответы клиентам: {stats['pain_points'].get('pain_messages', 0)}
📊 Работа с данными: {stats['pain_points'].get('pain_data', 0)}
👨‍🍼 Напоминания о дедлайнах: {stats['pain_points'].get('pain_deadlines', 0)}
📄 Формирование документов: {stats['pain_points'].get('pain_documents', 0)}
🔄 Копирование данных: {stats['pain_points'].get('pain_copying', 0)}
    """

    await update.message.reply_text(stats_text)


# ==================== ОБРАБОТЧИКИ КНОПОК ====================

async def start_quiz_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало опроса"""
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    update_user_step(user_id, 'question_1')

    await query.edit_message_text(
        QUESTION_1_MESSAGE,
        reply_markup=get_emotion_keyboard()
    )

    return QUESTION_1_EMOTION


async def emotion_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка ответа на вопрос об эмоциях"""
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    emotion = query.data  # emotion_tired, emotion_annoyed, emotion_confused

    # Сохраняем ответ
    save_answer(user_id, 'emotion', emotion)
    update_user_step(user_id, 'question_2')

    # Показываем промежуточный ответ
    response_text = EMOTION_RESPONSES.get(emotion, "Понял, идем дальше.")

    await query.edit_message_text(response_text)

    # Через секунду показываем следующий вопрос
    import asyncio
    await asyncio.sleep(1.5)

    await query.message.reply_text(
        QUESTION_2_MESSAGE,
        reply_markup=get_pain_point_keyboard()
    )

    return QUESTION_2_PAIN


async def pain_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка ответа на вопрос о проблеме"""
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    pain_point = query.data  # pain_messages, pain_data, etc.

    # Сохраняем ответ и в контекст для дальнейшего использования
    save_answer(user_id, 'pain_point', pain_point)
    context.user_data['pain_point'] = pain_point
    update_user_step(user_id, 'question_3')

    await query.edit_message_text(
        QUESTION_3_MESSAGE,
        reply_markup=get_time_keyboard()
    )

    return QUESTION_3_TIME


async def time_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка ответа на вопрос о времени"""
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    time_spent = query.data  # time_low, time_medium, time_high

    # Сохраняем ответ
    save_answer(user_id, 'time_spent', time_spent)
    update_user_step(user_id, 'show_insight')

    # Получаем pain_point из контекста
    pain_point = context.user_data.get('pain_point', 'pain_messages')

    # Генерируем персонализированный инсайт
    insight_text = get_insight_message(pain_point, time_spent)

    await query.edit_message_text(insight_text, parse_mode='Markdown')

    # Через 2 секунды показываем предложение
    import asyncio
    await asyncio.sleep(2)

    await query.message.reply_text(
        OFFER_MESSAGE,
        reply_markup=get_offer_keyboard(),
        parse_mode='Markdown'
    )

    return SHOW_OFFER


async def consultation_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Пользователь хочет консультацию"""
    query = update.callback_query
    await query.answer("Отлично! Отправляю заявку...")

    user_id = query.from_user.id
    user_data = get_user_data(user_id)

    # Отмечаем как конверсию
    mark_completed(user_id, conversion_status='converted')

    # Здесь можно отправить данные в CRM
    try:
        from crm_integration import send_lead_to_crm
        lead_info = {
            'user_id': user_id,
            'first_name': query.from_user.first_name,
            'username': query.from_user.username,
            'pain_point': user_data.pain_point if user_data else 'unknown',
            'time_spent': user_data.time_spent if user_data else 'unknown',
            'emotion': user_data.emotion if user_data else 'unknown'
        }
        send_lead_to_crm(lead_info)
        logger.info(f"Лид {user_id} отправлен в CRM")
    except Exception as e:
        logger.error(f"Ошибка отправки в CRM: {e}")

    await query.edit_message_text(CONVERSION_MESSAGE)

    return ConversationHandler.END


async def pdf_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Пользователь хочет PDF"""
    query = update.callback_query
    await query.answer("Отправляю PDF...")

    user_id = query.from_user.id

    # Отмечаем как завершенного, но не конвертированного
    mark_completed(user_id, conversion_status='pdf_downloaded')

    await query.edit_message_text(PDF_MESSAGE)

    # Здесь можно отправить реальный PDF файл
    # await query.message.reply_document(document=open('plan.pdf', 'rb'))

    return ConversationHandler.END


async def later_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Пользователь хочет вернуться позже"""
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    mark_completed(user_id, conversion_status='postponed')

    await query.edit_message_text(
        REMIND_LATER_MESSAGE,
        reply_markup=get_reminder_keyboard()
    )

    return COMPLETE


async def remind_later_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Пользователь нажал 'Позже' на начальном экране"""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        REMIND_LATER_MESSAGE,
        reply_markup=get_reminder_keyboard()
    )

    return COMPLETE


async def reminder_yes_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Пользователь согласился на напоминание"""
    query = update.callback_query
    await query.answer("Отлично! Напомню завтра!")

    user_id = query.from_user.id

    # Здесь можно настроить отложенное напоминание через JobQueue
    # context.job_queue.run_once(send_reminder, 86400, data=user_id)

    await query.edit_message_text(
        "✅ Супер! Напомню тебе завтра в это же время.\n\nДо встречи! 👋"
    )

    return ConversationHandler.END


async def reminder_no_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Пользователь отказался от напоминания"""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        THANK_YOU_MESSAGE,
        reply_markup=get_back_to_start_keyboard()
    )

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отмена разговора"""
    await update.message.reply_text(
        "Операция отменена. Используй /start чтобы начать заново."
    )
    return ConversationHandler.END


# Функция для отправки напоминания (для JobQueue)
async def send_reminder(context: ContextTypes.DEFAULT_TYPE):
    """Отправка напоминания пользователю"""
    job = context.job
    user_id = job.data

    await context.bot.send_message(
        chat_id=user_id,
        text="👋 Привет! Помнишь, ты хотел найти способ освободиться от рутины?\n\nГотов продолжить?",
        reply_markup=get_start_keyboard()
    )
