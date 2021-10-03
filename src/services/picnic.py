import datetime as dt
from typing import Optional

from sqlalchemy.orm import Session, joinedload

from src.models.picnic import Picnic, PicnicRegistration
from src.schemas.picnic import PicnicCreate, PicnicRegister


def get_by_id(db: Session, picnic_id: int):
    """Получение пикнина по идентификатору из БД

    Args:
        db: Сессия БД
        picnic_id: Идентификатор пикника

    Returns:
        Query пикника

    """

    return db.query(Picnic).filter(Picnic.id == picnic_id).first()


def get_picnics(db: Session, datetime: Optional[dt.datetime], past: bool) -> list:
    """Получение списка пикников из БД

    Args:
        db: Сессия БД
        datetime: Фильтр по времени пикника
        past: Фильтр прошедших пикников

    Returns:
      Список Query пикников

    """

    picnics = db.query(Picnic).options(joinedload(Picnic.users).joinedload(PicnicRegistration.user)).options(
        joinedload(Picnic.city))
    if datetime:
        picnics = picnics.filter(Picnic.time == datetime)
    if not past:
        picnics = picnics.filter(Picnic.time >= dt.datetime.now())
    return picnics.all()


def create_picnic(db: Session, picnic: PicnicCreate):
    """Создание записи пикника в БД

    Args:
        db: Сессия БД
        picnic: Схема создания пикника

    Returns:
        Запись пикника из БД

    """

    picnic_data = picnic.dict()
    picnic_post = Picnic(**picnic_data)
    db.add(picnic_post)
    db.commit()
    db.refresh(picnic_post)
    return picnic_post


def create_picnic_registration(db: Session, picnic_register: PicnicRegister, picnic_id: int):
    """Создание записи регистрации пользователя на пикник

    Args:
        db: Сессия БД
        picnic_register: Схема регистрации пикника
        picnic_id: Идентификатор пикника

    Returns:
      Запись регистрации пикника из БД

    """

    picnic_registration_data = picnic_register.dict()
    picnic_registration_post = PicnicRegistration(
        user_id=picnic_registration_data['user_id'],
        picnic_id=picnic_id
    )
    db.add(picnic_registration_post)
    db.commit()
    db.refresh(picnic_registration_post)
    return picnic_registration_post


def get_by_user_and_picnic(db: Session, picnic_id: int, user_id):
    """Получение записи регистрации пикника по идентификатору пикника и идентификатору пользователя

    Args:
        db: Сессия БД
        picnic_id: Идентификатор пикника
        user_id: Идентификатор пользователя

    Returns:
       Запись регистрации пикника из БД

    """

    return db.query(Picnic).filter(PicnicRegistration.picnic_id == picnic_id,
                                   PicnicRegistration.user_id == user_id).first()
