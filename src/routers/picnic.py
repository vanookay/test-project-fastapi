import datetime as dt
from typing import Any

from fastapi import APIRouter, Query

from src.db.database import SessionLocal
from src.models.city import City
from src.models.picnic import Picnic, PicnicRegistration

router: Any = APIRouter(
    tags=["picnic"],
    responses={404: {"Description": "Not found"}},
)


@router.get('/all-picnics/', summary='All Picnics', tags=['picnic'])
def all_picnics(datetime: dt.datetime = Query(default=None, description='Время пикника (по умолчанию не задано)'),
                past: bool = Query(default=True, description='Включая уже прошедшие пикники')):
    """
    Список всех пикников
    """
    picnics = SessionLocal().query(Picnic)
    if datetime is not None:
        picnics = picnics.filter(Picnic.time == datetime)
    if not past:
        picnics = picnics.filter(Picnic.time >= dt.datetime.now())

    return [{
        'id': pic.id,
        'city': SessionLocal().query(City).filter(City.id == pic.id).first().name,
        'time': pic.time,
        'users': [
            {
                'id': pr.user.id,
                'name': pr.user.name,
                'surname': pr.user.surname,
                'age': pr.user.age,
            }
            for pr in SessionLocal().query(PicnicRegistration).filter(PicnicRegistration.picnic_id == pic.id)],
    } for pic in picnics]


@router.get('/picnic-add/', summary='Picnic Add', tags=['picnic'])
def picnic_add(city_id: int = None, datetime: dt.datetime = None):
    p = Picnic(city_id=city_id, time=datetime)
    s = SessionLocal()
    s.add(p)
    s.commit()

    return {
        'id': p.id,
        'city': SessionLocal().query(City).filter(City.id == p.id).first().name,
        'time': p.time,
    }


@router.get('/picnic-register/', summary='Picnic Registration', tags=['picnic'])
def register_to_picnic(*_, **__, ):
    """
    Регистрация пользователя на пикник
    (Этот эндпойнт необходимо реализовать в процессе выполнения тестового задания)
    """
    # TODO: Сделать логику
    return ...
