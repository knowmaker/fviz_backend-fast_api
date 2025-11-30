# app/db/seed_data.py
import csv
from pathlib import Path

from sqlalchemy.orm import Session

from app.models.lt import LT


def seed_lt(db: Session, csv_path: str | None = None) -> None:
    """
    Заполняет таблицу lt данными из CSV-файла.
    По умолчанию ищет файл lt.csv в той же папке, где находится этот модуль.

    Если таблица lt уже содержит данные — повторно не заполняет.
    """

    # Если таблица уже содержит строки — ничего не делаем
    if db.query(LT).first():
        return

    if csv_path is None:
        # путь: app/db/lt.csv
        csv_path = Path(__file__).with_name("lt.csv")
    else:
        csv_path = Path(csv_path)

    if not csv_path.exists():
        raise FileNotFoundError(f"Файл с данными для lt не найден: {csv_path}")

    rows: list[LT] = []

    with csv_path.open(mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # В CSV должны быть поля: l_indicate, t_indicate
            lt = LT(
                l_indicate=int(row["l_indicate"]),
                t_indicate=int(row["t_indicate"]),
            )
            rows.append(lt)

    if rows:
        db.bulk_save_objects(rows)
        db.commit()
