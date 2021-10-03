import logging
from typing import Any

from fastapi import FastAPI

from src.api.routers import api_router
from src.db.database import Base, engine

logger = logging.getLogger(__name__)

logging.basicConfig(filename='info.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.WARNING)

# Создание таблиц в БД
Base.metadata.create_all(bind=engine)

app: Any = FastAPI(title="FastAPI TestProject Backend")

app.include_router(api_router)
