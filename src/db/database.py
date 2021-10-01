from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import sessionmaker

# Создание сессии
from src.config import settings

engine = create_engine(
    f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:5432/{settings.DB_NAME}",
    pool_pre_ping=True
)
SessionLocal: Any = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Подключение базы (с автоматической генерацией моделей)
@as_declarative()
class Base:
    id: Any
    __name__: str
