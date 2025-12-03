"""
Модуль для работы с базой данных
"""
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import DATABASE_URL

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


class User(Base):
    """Модель пользователя"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False)  # Telegram user_id
    username = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    created_at = Column(DateTime, default=datetime.now)
    current_step = Column(String(50))
    is_completed = Column(Boolean, default=False)

    # Ответы пользователя
    emotion = Column(String(50))  # Эмоциональное состояние
    pain_point = Column(String(50))  # Основная проблема
    time_spent = Column(String(50))  # Часы в неделю

    # Результаты
    conversion_status = Column(String(50))  # pending, contacted, converted
    lead_sent_to_crm = Column(Boolean, default=False)

    def __repr__(self):
        return f"<User {self.user_id} - {self.first_name}>"


class UserAnswer(Base):
    """Модель ответов пользователя (для детальной аналитики)"""
    __tablename__ = 'user_answers'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    question = Column(String(100))
    answer = Column(Text)
    timestamp = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Answer {self.user_id} - {self.question}>"


def init_db():
    """Инициализация базы данных"""
    Base.metadata.create_all(engine)
    print("✅ База данных инициализирована")


def get_or_create_user(user_id, username=None, first_name=None, last_name=None):
    """Получить или создать пользователя"""
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(user_id=user_id).first()

        if not user:
            user = User(
                user_id=user_id,
                username=username,
                first_name=first_name,
                last_name=last_name
            )
            session.add(user)
            session.commit()
            print(f"✅ Создан новый пользователь: {first_name} ({user_id})")

        return user
    finally:
        session.close()


def update_user_step(user_id, step):
    """Обновить текущий шаг пользователя"""
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(user_id=user_id).first()
        if user:
            user.current_step = step
            session.commit()
    finally:
        session.close()


def save_answer(user_id, field, value):
    """Сохранить ответ пользователя"""
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(user_id=user_id).first()
        if user:
            setattr(user, field, value)
            session.commit()

            # Также сохраняем в таблицу ответов для аналитики
            answer = UserAnswer(
                user_id=user_id,
                question=field,
                answer=value
            )
            session.add(answer)
            session.commit()
    finally:
        session.close()


def mark_completed(user_id, conversion_status='pending'):
    """Отметить прохождение теста как завершенное"""
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(user_id=user_id).first()
        if user:
            user.is_completed = True
            user.conversion_status = conversion_status
            session.commit()
    finally:
        session.close()


def get_user_data(user_id):
    """Получить данные пользователя"""
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(user_id=user_id).first()
        return user
    finally:
        session.close()


def get_statistics():
    """Получить статистику по боту"""
    session = SessionLocal()
    try:
        total_users = session.query(User).count()
        completed = session.query(User).filter_by(is_completed=True).count()

        # Популярные проблемы
        pain_points = {}
        for pain in ['pain_messages', 'pain_data', 'pain_deadlines', 'pain_documents', 'pain_copying']:
            count = session.query(User).filter_by(pain_point=pain).count()
            pain_points[pain] = count

        return {
            'total_users': total_users,
            'completed': completed,
            'completion_rate': (completed / total_users * 100) if total_users > 0 else 0,
            'pain_points': pain_points
        }
    finally:
        session.close()


if __name__ == '__main__':
    # Инициализация БД при запуске файла
    init_db()
