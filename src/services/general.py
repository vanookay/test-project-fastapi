from typing import Generator

from src.db.database import SessionLocal


def get_db() -> Generator:
    """Получение сессии БД

    Returns:
        Сессия БД

    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
