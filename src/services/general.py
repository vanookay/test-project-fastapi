from typing import Generator, Any

import requests
from fastapi import HTTPException
from starlette import status

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


class Client:
    """Класс-клиент для работы с запросами"""

    GET = 'get'
    POST = 'post'

    def __init__(self):
        """
        Инициализирует класс
        """

        self.session = requests.Session()

    def send_request(self, method: str, url: str) -> Any:
        """

        Args:
            method:
            url:

        Returns:

        """
        if method.lower() == self.GET:
            response = self.session.get(url)
        elif method.lower() == self.POST:
            response = self.session.post(url)
        else:
            raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

        if response.status_code != 200:
            response.raise_for_status()

        return response
