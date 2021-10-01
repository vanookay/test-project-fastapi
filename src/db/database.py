from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import sessionmaker

# Создание сессии
from src.config import settings

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI
)
SessionLocal: Any = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Подключение базы (с автоматической генерацией моделей)
@as_declarative()
class Base:
    id: Any
    __name__: str


Base.metadata.create_all(bind=engine)
