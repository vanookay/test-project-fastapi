from sqlalchemy import Column, Integer, String

from src.db.database import Base
from src.services.external_requests import GetWeatherRequest


class City(Base):
    """
    Город
    """
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    @property
    def weather(self) -> str:
        """
        Возвращает текущую погоду в этом городе
        """
        r = GetWeatherRequest()
        weather = r.get_weather(self.name)
        return weather

    def __repr__(self):
        return f'<Город "{self.name}">'
