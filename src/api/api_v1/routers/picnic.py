import datetime as dt
from typing import Any

from fastapi import APIRouter, Query, HTTPException

from src.db.database import SessionLocal
from src.models.city import City
from src.models.picnic import Picnic, PicnicRegistration
from src.models.user import User
from src.schemas.picnic import PicnicCreateRequest, PicnicRegisterRequest

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


@router.post('/picnic-add/', summary='Picnic Add', tags=['picnic'])
def picnic_add(picnic: PicnicCreateRequest):
    city = SessionLocal().query(City).filter(City.id == picnic.city_id).first()
    if not city:
        raise HTTPException(status_code=400, detail='Город с таким идентификатором не существует')

    p = Picnic(city_id=picnic.city_id, time=picnic.time)
    s = SessionLocal()
    s.add(p)
    s.commit()

    return {
        'id': p.id,
        'city': city.name,
        'time': p.time,
    }


@router.post('/picnic-register/', summary='Picnic Registration', tags=['picnic'])
def register_to_picnic(picnic_register: PicnicRegisterRequest):
    """Регистрация пользователя на пикник"""

    user = SessionLocal().query(User).filter(User.id == picnic_register.user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail='Пользователь с таким идентификатором не существует')
    if not SessionLocal().query(Picnic).filter(Picnic.id == picnic_register.picnic_id).first():
        raise HTTPException(status_code=400, detail='Пикник с таким идентификатором не существует')
    picnic_reg = PicnicRegistration(user_id=picnic_register.user_id, picnic_id=picnic_register.picnic_id)
    s = SessionLocal()
    s.add(picnic_reg)
    s.commit()
    return {
        'id': picnic_reg.id,
        'user': f"{user.surname} {user.name}",
        'picnic': picnic_register.picnic_id,
    }
