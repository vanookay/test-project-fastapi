from typing import Any

from fastapi import APIRouter, HTTPException, Query

from src.db.database import SessionLocal
from src.models.city import City
from src.services.external_requests import CheckCityExisting

router: Any = APIRouter(
    tags=["city"],
    responses={404: {"Description": "Not found"}},
)


@router.post('/city/', summary='Create City', description='Создание города по его названию')
def create_city(city: str = Query(description="Название города", default=None)):
    if city is None:
        raise HTTPException(status_code=400, detail='Параметр city должен быть указан')
    check = CheckCityExisting()
    if not check.check_existing(city):
        raise HTTPException(status_code=400, detail='Параметр city должен быть существующим городом')

    city_object = SessionLocal().query(City).filter(City.name == city.capitalize()).first()
    if city_object is None:
        city_object = City(name=city.capitalize())
        s = SessionLocal()
        s.add(city_object)
        s.commit()

    return {'id': city_object.id, 'name': city_object.name, 'weather': city_object.weather}


@router.get('/city/', summary='Get Cities')
def cities_list(q: str = Query(description="Название города", default=None)):
    """
    Получение списка городов
    """
    cities = SessionLocal().query(City).all()

    return [{'id': city.id, 'name': city.name, 'weather': city.weather} for city in cities]
