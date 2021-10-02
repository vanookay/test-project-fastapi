from typing import Any

from fastapi import FastAPI

from src.api.routers import api_router
from src.db.database import Base, engine

# Создание таблиц в БД
Base.metadata.create_all(bind=engine)

app: Any = FastAPI(title="FastAPI TestProject Backend")

app.include_router(api_router)
