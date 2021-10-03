import datetime as dt
from typing import Any, List

from fastapi import APIRouter, Query, HTTPException, Depends
from sqlalchemy.orm import Session

from src.config import settings
from src.schemas.picnic import PicnicCreate, PicnicRegister, Picnics, PicnicResponse, PicnicRegisterResponse
from src.services.city import get_by_id as get_city_by_id
from src.services.general import get_db
from src.services.picnic import get_picnics, create_picnic, get_by_id as get_picnic_by_id, create_picnic_registration, \
    get_by_user_and_picnic
from src.services.users import get_by_id as get_user_by_id

router: Any = APIRouter(
    tags=["picnic"],
    responses={
        404: {"Description": "Не найдено"}
    },
)


@router.get('/picnic/', summary='All Picnics', tags=['picnic'], response_model=List[Picnics])
def all_picnics(
        db: Session = Depends(get_db),
        datetime: dt.datetime = Query(default=None, description='Время пикника (по умолчанию не задано)'),
        past: bool = Query(default=True, description='Включая уже прошедшие пикники')
) -> List:
    """
    Получение списка пикников
    """

    return get_picnics(db=db, datetime=datetime, past=past)


@router.post('/picnic/', summary='Picnic Add', tags=['picnic'], response_model=PicnicResponse)
def picnic_add(
        picnic: PicnicCreate,
        db: Session = Depends(get_db)
) -> Any:
    """
    Создание пикника
    """

    if picnic.time <= dt.datetime.now(settings.tzinfo):
        raise HTTPException(status_code=400, detail='Время проведения пикника не может быть меньше текущей даты')

    city = get_city_by_id(db=db, city_id=picnic.city_id)
    if not city:
        raise HTTPException(status_code=404, detail='Город с таким идентификатором не существует')

    return create_picnic(db=db, picnic=picnic)


@router.post('/picnic/{picnic_id}/users/', summary='Picnic User Registration', tags=['picnic'],
             response_model=PicnicRegisterResponse)
def register_to_picnic(
        picnic_id: int,
        picnic_register: PicnicRegister,
        db: Session = Depends(get_db)
):
    """
    Регистрация пользователя на пикник
    """

    if not get_user_by_id(db=db, user_id=picnic_register.user_id):
        raise HTTPException(status_code=404, detail='Пользователь с таким идентификатором не существует')

    picnic = get_picnic_by_id(db=db, picnic_id=picnic_id)
    if not picnic:
        raise HTTPException(status_code=404, detail='Пикник с таким идентификатором не существует')

    if picnic.time <= dt.datetime.now():
        raise HTTPException(status_code=400, detail='Регистрация на пикник закрыта (пикник проведен)')

    if get_by_user_and_picnic(db=db, picnic_id=picnic_id, user_id=picnic_register.user_id):
        raise HTTPException(status_code=400, detail='Пользователь уже присутствует на пикнике')

    return create_picnic_registration(db=db, picnic_register=picnic_register, picnic_id=picnic_id)
