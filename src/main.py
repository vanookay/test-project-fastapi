from typing import Any

from fastapi import FastAPI

from src.db.database import Base, engine
from src.routers import city, picnic, user

# Создание таблиц в БД
Base.metadata.create_all(bind=engine)

app: Any = FastAPI(title="FastAPI TestProject Backend")

app.include_router(city.router)
app.include_router(picnic.router)
app.include_router(user.router)
