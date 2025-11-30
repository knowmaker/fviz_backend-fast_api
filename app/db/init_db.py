# app/db/init_db.py
from app.db.session import engine, SessionLocal
from app.models import Base  # тянет все модели через __init__.py
from app.db.seed_data import seed_lt


def init_db() -> None:
    """
    Создаёт все таблицы в БД и заполняет их начальными данными.
    Сейчас: только таблица lt из CSV.
    """
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        seed_lt(db)
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
