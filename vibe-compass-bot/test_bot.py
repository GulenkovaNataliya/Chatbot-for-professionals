"""
Скрипт для тестирования функциональности бота
Запуск: python test_bot.py
"""
from database import *
from messages import get_insight_message
import random


def test_database():
    """Тест работы с базой данных"""
    print("\n=== ТЕСТ БАЗЫ ДАННЫХ ===")

    try:
        # Инициализация
        init_db()
        print("✅ Инициализация БД")

        # Создание тестового пользователя
        user = get_or_create_user(
            user_id=12345,
            username='test_user',
            first_name='Тест',
            last_name='Тестович'
        )
        print(f"✅ Создание пользователя: {user.first_name}")

        # Сохранение ответов
        save_answer(12345, 'emotion', 'emotion_tired')
        save_answer(12345, 'pain_point', 'pain_messages')
        save_answer(12345, 'time_spent', 'time_high')
        print("✅ Сохранение ответов")

        # Получение данных
        user_data = get_user_data(12345)
        print(f"✅ Получение данных: {user_data.emotion}")

        # Статистика
        stats = get_statistics()
        print(f"✅ Статистика: {stats['total_users']} пользователей")

        print("\n✅ ВСЕ ТЕСТЫ БД ПРОЙДЕНЫ\n")
        return True

    except Exception as e:
        print(f"\n❌ ОШИБКА В ТЕСТАХ БД: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_messages():
    """Тест генерации сообщений"""
    print("\n=== ТЕСТ ГЕНЕРАЦИИ СООБЩЕНИЙ ===")

    try:
        pain_points = ['pain_messages', 'pain_data', 'pain_deadlines', 'pain_documents', 'pain_copying']
        time_variants = ['time_low', 'time_medium', 'time_high']

        for pain in pain_points:
            for time in time_variants:
                message = get_insight_message(pain, time)
                if message and len(message) > 50:
                    print(f"✅ {pain} + {time}: {len(message)} символов")
                else:
                    print(f"❌ {pain} + {time}: Ошибка генерации")
                    return False

        print("\n✅ ВСЕ СООБЩЕНИЯ СГЕНЕРИРОВАНЫ\n")
        return True

    except Exception as e:
        print(f"\n❌ ОШИБКА В ГЕНЕРАЦИИ СООБЩЕНИЙ: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def generate_test_data():
    """Генерация тестовых данных для демонстрации"""
    print("\n=== ГЕНЕРАЦИЯ ТЕСТОВЫХ ДАННЫХ ===")

    try:
        emotions = ['emotion_tired', 'emotion_annoyed', 'emotion_confused']
        pains = ['pain_messages', 'pain_data', 'pain_deadlines', 'pain_documents', 'pain_copying']
        times = ['time_low', 'time_medium', 'time_high']
        statuses = ['pending', 'converted', 'pdf_downloaded', 'postponed']

        first_names = ['Алексей', 'Мария', 'Дмитрий', 'Анна', 'Сергей', 'Елена', 'Иван', 'Ольга']
        last_names = ['Иванов', 'Петрова', 'Сидоров', 'Козлова', 'Смирнов', 'Новикова']

        for i in range(1, 21):
            user_id = 1000 + i
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)

            # Создаем пользователя
            user = get_or_create_user(
                user_id=user_id,
                username=f'user{i}',
                first_name=first_name,
                last_name=last_name
            )

            # Добавляем ответы
            save_answer(user_id, 'emotion', random.choice(emotions))
            save_answer(user_id, 'pain_point', random.choice(pains))
            save_answer(user_id, 'time_spent', random.choice(times))

            # Отмечаем как завершенного с случайным статусом
            if random.random() > 0.3:  # 70% завершили
                mark_completed(user_id, random.choice(statuses))

            print(f"✅ Создан тестовый пользователь {i}: {first_name} {last_name}")

        print(f"\n✅ СОЗДАНО 20 ТЕСТОВЫХ ПОЛЬЗОВАТЕЛЕЙ\n")

        # Показываем статистику
        stats = get_statistics()
        print("📊 СТАТИСТИКА:")
        print(f"   Всего пользователей: {stats['total_users']}")
        print(f"   Завершили тест: {stats['completed']}")
        print(f"   Конверсия: {stats['completion_rate']:.1f}%")
        print(f"\n   Популярные проблемы:")
        for pain, count in stats['pain_points'].items():
            if count > 0:
                print(f"   - {pain}: {count}")

        return True

    except Exception as e:
        print(f"\n❌ ОШИБКА ГЕНЕРАЦИИ ДАННЫХ: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_keyboards():
    """Тест клавиатур"""
    print("\n=== ТЕСТ КЛАВИАТУР ===")

    try:
        from keyboards import (
            get_start_keyboard,
            get_emotion_keyboard,
            get_pain_point_keyboard,
            get_time_keyboard,
            get_offer_keyboard
        )

        keyboards = [
            ('start', get_start_keyboard),
            ('emotion', get_emotion_keyboard),
            ('pain_point', get_pain_point_keyboard),
            ('time', get_time_keyboard),
            ('offer', get_offer_keyboard)
        ]

        for name, func in keyboards:
            keyboard = func()
            if keyboard and hasattr(keyboard, 'inline_keyboard'):
                button_count = sum(len(row) for row in keyboard.inline_keyboard)
                print(f"✅ Клавиатура '{name}': {button_count} кнопок")
            else:
                print(f"❌ Клавиатура '{name}': Ошибка создания")
                return False

        print("\n✅ ВСЕ КЛАВИАТУРЫ РАБОТАЮТ\n")
        return True

    except Exception as e:
        print(f"\n❌ ОШИБКА В КЛАВИАТУРАХ: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_config():
    """Тест конфигурации"""
    print("\n=== ТЕСТ КОНФИГУРАЦИИ ===")

    try:
        from config import TELEGRAM_BOT_TOKEN, DATABASE_URL

        if not TELEGRAM_BOT_TOKEN:
            print("⚠️  TELEGRAM_BOT_TOKEN не установлен")
        elif TELEGRAM_BOT_TOKEN == 'your_bot_token_here':
            print("⚠️  TELEGRAM_BOT_TOKEN содержит значение по умолчанию")
            print("   Замените его в файле .env")
        else:
            print(f"✅ TELEGRAM_BOT_TOKEN установлен ({len(TELEGRAM_BOT_TOKEN)} символов)")

        if DATABASE_URL:
            print(f"✅ DATABASE_URL: {DATABASE_URL}")
        else:
            print("⚠️  DATABASE_URL не установлен")

        print("\n✅ КОНФИГУРАЦИЯ ПРОВЕРЕНА\n")
        return True

    except Exception as e:
        print(f"\n❌ ОШИБКА В КОНФИГУРАЦИИ: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def interactive_test():
    """Интерактивное тестирование генерации инсайтов"""
    print("\n=== ИНТЕРАКТИВНОЕ ТЕСТИРОВАНИЕ ===")
    print("\nВыберите проблему:")
    print("1. Ответы на повторяющиеся вопросы (pain_messages)")
    print("2. Сведение данных из таблиц (pain_data)")
    print("3. Напоминания о дедлайнах (pain_deadlines)")
    print("4. Формирование документов (pain_documents)")
    print("5. Копирование данных (pain_copying)")

    pain_map = {
        '1': 'pain_messages',
        '2': 'pain_data',
        '3': 'pain_deadlines',
        '4': 'pain_documents',
        '5': 'pain_copying'
    }

    pain_choice = input("\nВаш выбор (1-5): ").strip()
    pain = pain_map.get(pain_choice, 'pain_messages')

    print("\nВыберите время:")
    print("1. Меньше 5 часов (time_low)")
    print("2. 5-10 часов (time_medium)")
    print("3. Больше 10 часов (time_high)")

    time_map = {
        '1': 'time_low',
        '2': 'time_medium',
        '3': 'time_high'
    }

    time_choice = input("\nВаш выбор (1-3): ").strip()
    time = time_map.get(time_choice, 'time_medium')

    print("\n" + "="*60)
    print("СГЕНЕРИРОВАННОЕ СООБЩЕНИЕ:")
    print("="*60)
    message = get_insight_message(pain, time)
    print(message)
    print("="*60 + "\n")


def main_menu():
    """Главное меню тестирования"""
    while True:
        print("\n" + "="*60)
        print("  🧪 МЕНЮ ТЕСТИРОВАНИЯ БОТА")
        print("="*60)
        print("\n1. Запустить все тесты")
        print("2. Тест базы данных")
        print("3. Тест генерации сообщений")
        print("4. Тест клавиатур")
        print("5. Тест конфигурации")
        print("6. Сгенерировать тестовые данные")
        print("7. Интерактивный тест инсайтов")
        print("8. Показать статистику БД")
        print("0. Выход")

        choice = input("\nВыберите опцию: ").strip()

        if choice == '1':
            results = [
                test_config(),
                test_database(),
                test_messages(),
                test_keyboards()
            ]
            if all(results):
                print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
            else:
                print("\n⚠️  Некоторые тесты не прошли")

        elif choice == '2':
            test_database()
        elif choice == '3':
            test_messages()
        elif choice == '4':
            test_keyboards()
        elif choice == '5':
            test_config()
        elif choice == '6':
            confirm = input("Создать 20 тестовых пользователей? (y/n): ")
            if confirm.lower() == 'y':
                generate_test_data()
        elif choice == '7':
            interactive_test()
        elif choice == '8':
            stats = get_statistics()
            print("\n📊 СТАТИСТИКА БАЗЫ ДАННЫХ:")
            print(f"   Всего пользователей: {stats['total_users']}")
            print(f"   Завершили тест: {stats['completed']}")
            print(f"   Конверсия: {stats['completion_rate']:.1f}%")
            print(f"\n   Популярные проблемы:")
            for pain, count in stats['pain_points'].items():
                print(f"   - {pain}: {count}")
        elif choice == '0':
            print("\nДо свидания! 👋\n")
            break
        else:
            print("\n⚠️  Неверный выбор, попробуйте снова")


if __name__ == '__main__':
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Тестирование прервано\n")
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
