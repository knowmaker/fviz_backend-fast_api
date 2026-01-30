# app/db/init_db.py
from app.db.session import engine, SessionLocal
from app.models import Base  # тянет все модели через __init__.py
from app.db.seed_data import seed_lt, seed_gk, seed_system_types, seed_quantities, seed_law_groups


def init_db() -> None:
    """
    Создаёт все таблицы в БД и заполняет их начальными данными.
    Сейчас: только таблица lt из CSV.
    """
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        seed_system_types(db)
        seed_lt(db)
        seed_gk(db)
        seed_quantities(db)
        seed_law_groups(db)
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
