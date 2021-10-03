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
    picnics = db.query(Picnic).options(joinedload(Picnic.users).joinedload(PicnicRegistration.user)).options(
        joinedload(Picnic.city))
    if datetime:
        picnics = picnics.filter(Picnic.time == datetime)
    if not past:
        picnics = picnics.filter(Picnic.time >= dt.datetime.now())
    return picnics.all()


def create_picnic(db: Session, picnic: PicnicCreate):
    picnic_data = picnic.dict()
    picnic_post = Picnic(**picnic_data)
    db.add(picnic_post)
    db.commit()
    db.refresh(picnic_post)
    return picnic_post


def create_picnic_registration(db: Session, picnic_register: PicnicRegister, picnic_id: int):
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
    return db.query(Picnic).filter(PicnicRegistration.picnic_id == picnic_id,
                                   PicnicRegistration.user_id == user_id).first()
