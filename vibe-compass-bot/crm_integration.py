"""
Интеграция с CRM системами
Здесь реализованы функции для отправки лидов в различные CRM
"""
import requests
import logging
from config import AMOCRM_TOKEN, AMOCRM_DOMAIN

logger = logging.getLogger(__name__)


def send_lead_to_crm(lead_info):
    """
    Отправка лида в CRM систему

    Args:
        lead_info (dict): Информация о лиде
            - user_id: Telegram ID
            - first_name: Имя
            - username: Username
            - pain_point: Основная проблема
            - time_spent: Время, потраченное на рутину
            - emotion: Эмоциональное состояние
    """

    # Выбираем CRM систему на основе конфигурации
    if AMOCRM_TOKEN and AMOCRM_TOKEN != 'your_amocrm_token_here':
        return send_to_amocrm(lead_info)
    else:
        # Если CRM не настроена, просто логируем
        logger.info(f"📋 Новый лид (CRM не настроена): {lead_info}")
        return {'success': True, 'message': 'CRM не настроена, лид залогирован'}


def send_to_amocrm(lead_info):
    """Отправка лида в AmoCRM"""
    try:
        url = f"https://{AMOCRM_DOMAIN}/api/v4/leads"

        headers = {
            'Authorization': f'Bearer {AMOCRM_TOKEN}',
            'Content-Type': 'application/json'
        }

        # Формируем читаемое описание проблемы
        pain_points_map = {
            'pain_messages': 'Ответы на повторяющиеся вопросы клиентов',
            'pain_data': 'Сведение данных из таблиц',
            'pain_deadlines': 'Напоминания о дедлайнах команде',
            'pain_documents': 'Формирование документов',
            'pain_copying': 'Копирование данных между системами'
        }

        time_map = {
            'time_low': 'Меньше 5 часов в неделю',
            'time_medium': '5-10 часов в неделю',
            'time_high': 'Больше 10 часов в неделю'
        }

        emotion_map = {
            'emotion_tired': 'Выжатый как лимон',
            'emotion_annoyed': 'Раздраженный',
            'emotion_confused': 'Запутавшийся'
        }

        pain_text = pain_points_map.get(lead_info.get('pain_point', ''), 'Не указано')
        time_text = time_map.get(lead_info.get('time_spent', ''), 'Не указано')
        emotion_text = emotion_map.get(lead_info.get('emotion', ''), 'Не указано')

        # Данные лида
        lead_data = [{
            'name': f"Вайб-лид: {lead_info.get('first_name', 'Неизвестно')}",
            'price': 0,
            '_embedded': {
                'contacts': [{
                    'first_name': lead_info.get('first_name', ''),
                    'custom_fields_values': [
                        {
                            'field_code': 'PHONE',
                            'values': [{'value': f"Telegram: @{lead_info.get('username', 'no_username')}"}]
                        }
                    ]
                }]
            },
            'custom_fields_values': [
                {
                    'field_name': 'Основная проблема',
                    'values': [{'value': pain_text}]
                },
                {
                    'field_name': 'Время на рутину',
                    'values': [{'value': time_text}]
                },
                {
                    'field_name': 'Эмоциональное состояние',
                    'values': [{'value': emotion_text}]
                },
                {
                    'field_name': 'Telegram ID',
                    'values': [{'value': str(lead_info.get('user_id', ''))}]
                }
            ]
        }]

        response = requests.post(url, json=lead_data, headers=headers, timeout=10)

        if response.status_code in [200, 201]:
            logger.info(f"✅ Лид успешно отправлен в AmoCRM: {lead_info.get('first_name')}")
            return {'success': True, 'response': response.json()}
        else:
            logger.error(f"❌ Ошибка отправки в AmoCRM: {response.status_code} - {response.text}")
            return {'success': False, 'error': response.text}

    except Exception as e:
        logger.error(f"❌ Исключение при отправке в AmoCRM: {e}")
        return {'success': False, 'error': str(e)}


def send_to_bitrix24(lead_info):
    """Отправка лида в Bitrix24"""
    # Здесь можно реализовать интеграцию с Bitrix24
    logger.info("Bitrix24 интеграция еще не реализована")
    pass


def send_to_google_sheets(lead_info):
    """
    Отправка лида в Google Sheets
    Простое решение для старта без настройки CRM
    """
    try:
        from datetime import datetime

        # Здесь нужно настроить Google Sheets API
        # Для примера просто логируем

        lead_row = [
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            lead_info.get('first_name', ''),
            lead_info.get('username', ''),
            lead_info.get('user_id', ''),
            lead_info.get('pain_point', ''),
            lead_info.get('time_spent', ''),
            lead_info.get('emotion', '')
        ]

        logger.info(f"📊 Лид для Google Sheets: {lead_row}")

        # Здесь должна быть логика добавления в таблицу
        # Пример: sheet.append_row(lead_row)

        return {'success': True, 'message': 'Logged for Google Sheets'}

    except Exception as e:
        logger.error(f"Ошибка отправки в Google Sheets: {e}")
        return {'success': False, 'error': str(e)}


def send_notification_to_telegram(admin_chat_id, lead_info):
    """
    Отправка уведомления админу в Telegram о новом лиде
    """
    from telegram import Bot
    from config import TELEGRAM_BOT_TOKEN

    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)

        message = f"""
🎯 **Новый лид из Вайб-Компаса!**

👤 Имя: {lead_info.get('first_name', 'Неизвестно')}
📱 Telegram: @{lead_info.get('username', 'нет username')}
🆔 ID: {lead_info.get('user_id', '')}

📋 Проблема: {lead_info.get('pain_point', '')}
⏰ Время на рутину: {lead_info.get('time_spent', '')}
😔 Состояние: {lead_info.get('emotion', '')}
        """

        bot.send_message(chat_id=admin_chat_id, text=message, parse_mode='Markdown')
        logger.info(f"✅ Уведомление отправлено админу")

    except Exception as e:
        logger.error(f"❌ Ошибка отправки уведомления: {e}")


# ==================== WEBHOOK для получения обновлений из CRM ====================

def setup_webhook(webhook_url):
    """
    Настройка webhook для получения обновлений из CRM
    Например, когда менеджер обработал лида
    """
    # Здесь можно настроить webhook в CRM системе
    pass
