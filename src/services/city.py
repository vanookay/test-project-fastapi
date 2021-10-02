from typing import Optional

from sqlalchemy.orm import Session

from src.models.city import City
from src.schemas.city import CityCreate
from src.services.external_requests import CheckCityExisting


def get_by_name(db: Session, name: str):
    """Получение города по наименованию из БД

    Args:
        db: Сессия БД
        name: Наименование города

    Returns:
        Query города

    """

    return db.query(City).filter(City.name == name.capitalize()).first()


def check_existing(name: str) -> bool:
    """Сервис проверки города на существование

    Args:
        name: Наименование города

    Returns:
        Булево значение

    """

    check = CheckCityExisting()
    return check.check_existing(city=name)


def get_cities(db: Session, q: Optional[str]) -> list:
    """Получение списка городов

    Args:
        db: Сессия БД
        q: Наименование города

    Returns:
        Список городов из БД

    """

    cities = db.query(City)
    if q:
        cities = cities.filter(City.name == q.capitalize())
    return cities.all()


def city_create(db: Session, city: CityCreate):
    """Создание записи города

    Args:
        db: Сессия БД
        city: Объект города

    Returns:
        Созданный объект города из БД

    """

    city_data = city.dict()
    city_post = City(name=city_data['name'].capitalize())
    db.add(city_post)
    db.commit()
    db.refresh(city_post)
    return city_post
