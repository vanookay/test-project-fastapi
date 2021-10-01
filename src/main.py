from typing import Any

from fastapi import FastAPI

from src.routers import city, picnic, user

app: Any = FastAPI(title="FastAPI TestProject Backend")
app.include_router(city.router)
app.include_router(picnic.router)
app.include_router(user.router)
