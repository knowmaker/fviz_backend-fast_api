# app/db/seed_data.py
import csv
from pathlib import Path

from sqlalchemy.orm import Session

from app.models.lt import LT
from app.models.system_type import SystemType
from app.models.gk import GK
from app.models.quantity import Quantity
from app.models.law_group import LawGroup

def seed_lt(db: Session, csv_path: str | None = None) -> None:
    """
    Заполняет таблицу lt данными из CSV-файла.
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
        raise FileNotFoundError(f"Файл lt.csv не найден: {csv_path}")

    rows: list[LT] = []

    with csv_path.open(mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            lt = LT(
                l_indicate=int(row["l_indicate"]),
                t_indicate=int(row["t_indicate"]),
            )
            rows.append(lt)

    if rows:
        db.bulk_save_objects(rows)
        db.commit()

def seed_system_types(db: Session) -> None:
    """
    Заполняет таблицу system_types.
    Если таблица НЕ пуста — ничего не делает.
    """
    if db.query(SystemType).first():
        return

    system_types = [
        SystemType(name="MLTI"),
        SystemType(name="LTM"),
    ]

    db.add_all(system_types)
    db.commit()

def seed_gk(db: Session, csv_path: str | None = None) -> None:
    """
    Заполняет таблицу gk из CSV.
    Логика как у lt: если таблица НЕ пуста — ничего не делаем.
    system_type_id всегда = 1.
    """
    if db.query(GK).first():
        return

    if csv_path is None:
        # app/db/gk.csv
        csv_path = Path(__file__).with_name("gk.csv")
    else:
        csv_path = Path(csv_path)

    if not csv_path.exists():
        raise FileNotFoundError(f"Файл gk.csv не найден: {csv_path}")

    rows: list[GK] = []

    with csv_path.open(mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(
                GK(
                    g_indicate=int(row["g_indicate"]),
                    k_indicate=int(row["k_indicate"]),
                    name=row["name"],
                    color=row["color"],
                    system_type_id=row["system_type_id"],
                )
            )

    if rows:
        db.bulk_save_objects(rows)
        db.commit()

def seed_quantities(db: Session, csv_path: str | None = None) -> None:
    if db.query(Quantity).first():
        return

    if csv_path is None:
        csv_path = Path(__file__).with_name("quantities.csv")
    else:
        csv_path = Path(csv_path)

    if not csv_path.exists():
        raise FileNotFoundError(f"Файл quantities.csv не найден: {csv_path}")

    rows: list[Quantity] = []

    with csv_path.open(mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(
                Quantity(
                    symbol=row["symbol"],
                    name=row["name"],
                    unit=row["unit"],
                    m_indicate=row["m_indicate"],
                    l_indicate=row["l_indicate"],
                    t_indicate=row["t_indicate"],
                    i_indicate=row["i_indicate"],
                    lt_id=int(row["lt_id"]),
                    gk_id=int(row["gk_id"]),
                    system_type_id=1,
                )
            )

    if rows:
        db.bulk_save_objects(rows)
        db.commit()


def seed_law_groups(db: Session, csv_path: str | None = None) -> None:
    """
    Логика как у lt: если таблица НЕ пуста — ничего не делаем.
    system_type_id всегда = 1.
    """
    if db.query(LawGroup).first():
        return

    if csv_path is None:
        # app/db/law_groups.csv
        csv_path = Path(__file__).with_name("law_groups.csv")
    else:
        csv_path = Path(csv_path)

    if not csv_path.exists():
        raise FileNotFoundError(f"Файл law_groups.csv не найден: {csv_path}")

    rows: list[LawGroup] = []

    with csv_path.open(mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(
                LawGroup(
                    name=row["name"],
                    color=row["color"],
                    system_type_id=1,
                )
            )

    if rows:
        db.bulk_save_objects(rows)
        db.commit()