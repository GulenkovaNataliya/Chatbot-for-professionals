"""
Скрипт для первоначальной настройки бота
Запустите его перед первым запуском: python setup.py
"""
import os
import sys


def print_header(text):
    """Красивый заголовок"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")


def check_python_version():
    """Проверка версии Python"""
    print_header("Проверка версии Python")

    if sys.version_info < (3, 8):
        print("❌ Ошибка: Требуется Python 3.8 или выше")
        print(f"   Ваша версия: {sys.version}")
        return False

    print(f"✅ Python {sys.version.split()[0]} - OK")
    return True


def check_dependencies():
    """Проверка установленных зависимостей"""
    print_header("Проверка зависимостей")

    required_packages = [
        'telegram',
        'sqlalchemy',
        'dotenv',
        'requests'
    ]

    missing = []

    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} - установлен")
        except ImportError:
            print(f"❌ {package} - не найден")
            missing.append(package)

    if missing:
        print("\n⚠️  Некоторые пакеты не установлены!")
        print("   Выполните: pip install -r requirements.txt")
        return False

    return True


def create_env_file():
    """Создание файла .env"""
    print_header("Настройка .env файла")

    if os.path.exists('.env'):
        print("⚠️  Файл .env уже существует")
        overwrite = input("   Перезаписать? (y/n): ").lower().strip()
        if overwrite != 'y':
            print("   Пропускаем создание .env")
            return True

    print("\n📝 Для работы бота нужен токен от @BotFather")
    print("   1. Откройте Telegram и найдите @BotFather")
    print("   2. Отправьте команду /newbot")
    print("   3. Следуйте инструкциям")
    print("   4. Скопируйте полученный токен\n")

    token = input("Введите токен бота (или Enter для пропуска): ").strip()

    env_content = f"""# Telegram Bot Token (получите у @BotFather)
TELEGRAM_BOT_TOKEN={token if token else 'your_bot_token_here'}

# CRM Integration (опционально)
AMOCRM_TOKEN=your_amocrm_token_here
AMOCRM_DOMAIN=yourdomain.amocrm.ru

# Database
DATABASE_URL=sqlite:///vibe_compass.db
"""

    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)

    if token:
        print("\n✅ Файл .env создан с вашим токеном")
    else:
        print("\n⚠️  Файл .env создан, но токен не указан")
        print("   Отредактируйте файл .env и добавьте токен перед запуском бота")

    return True


def init_database():
    """Инициализация базы данных"""
    print_header("Инициализация базы данных")

    try:
        from database import init_db
        init_db()
        print("✅ База данных успешно инициализирована")
        return True
    except Exception as e:
        print(f"❌ Ошибка при инициализации БД: {e}")
        return False


def test_bot_import():
    """Проверка импорта модулей бота"""
    print_header("Проверка модулей бота")

    modules = [
        'config',
        'database',
        'messages',
        'keyboards',
        'handlers',
        'bot'
    ]

    all_ok = True

    for module in modules:
        try:
            __import__(module)
            print(f"✅ {module}.py - OK")
        except Exception as e:
            print(f"❌ {module}.py - Ошибка: {e}")
            all_ok = False

    return all_ok


def print_final_instructions():
    """Финальные инструкции"""
    print_header("Готово к запуску!")

    print("🚀 Для запуска бота выполните:")
    print("   python bot.py")
    print()
    print("📚 Полезные команды:")
    print("   python database.py      - переинициализация БД")
    print("   /start                  - команда для пользователей")
    print("   /stats                  - статистика (в боте)")
    print("   /help                   - справка (в боте)")
    print()
    print("📖 Документация:")
    print("   README.md               - полная инструкция")
    print("   QUICKSTART.md           - быстрый старт")
    print("   LOCALIZATION.md         - перевод на другие языки")
    print()
    print("💡 Для перевода на греческий:")
    print("   Откройте handlers.py")
    print("   Измените: from messages import *")
    print("   На:       from messages_el import *")
    print()


def main():
    """Главная функция установки"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║         🤖 Вайб-Компас Освобождения - Установка         ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)

    steps = [
        ("Проверка Python", check_python_version),
        ("Проверка зависимостей", check_dependencies),
        ("Создание .env", create_env_file),
        ("Инициализация БД", init_database),
        ("Проверка модулей", test_bot_import)
    ]

    failed = []

    for step_name, step_func in steps:
        if not step_func():
            failed.append(step_name)

    print("\n" + "=" * 60)

    if failed:
        print("\n⚠️  Установка завершена с ошибками:")
        for fail in failed:
            print(f"   ❌ {fail}")
        print("\nИсправьте ошибки перед запуском бота")
    else:
        print("\n✅ Установка успешно завершена!")
        print_final_instructions()

    print("=" * 60 + "\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Установка прервана пользователем")
    except Exception as e:
        print(f"\n\n❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
