# app/db/init_db.py
from app.db.session import engine
from app.models import Base  # тянет все модели через __init__.py


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
