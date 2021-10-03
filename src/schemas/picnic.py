import datetime as dt
from typing import Optional, List

from pydantic import BaseModel, Field

from src.schemas.city import CityBaseInDB
from src.schemas.user import User, UserNameSurname


class PicnicRegistrationBase(BaseModel):
    user_id: int = Field(..., title="Идентификатор пользователя")
    picnic_id: int = Field(..., title="Идентификатор пикника")


class PicnicRegistration(PicnicRegistrationBase):
    id: Optional[int] = Field(..., title="Наименование регистрации на пикник")

    class Config:
        orm_mode: bool = True


class PicnicRegistrationUsers(BaseModel):
    user: User = Field(..., title="Объект пользователя")

    class Config:
        orm_mode: bool = True


class PicnicBase(BaseModel):
    city_id: int = Field(..., title="Идентификатор города")
    time: dt.datetime = Field(..., title="Время проведения пикника")


class Picnic(PicnicBase):
    id: Optional[int] = Field(..., title="Идентификатор пикника")

    class Config:
        orm_mode: bool = True


class PicnicResponse(BaseModel):
    id: int = Field(..., title="Идентификатор пикника")
    time: dt.datetime = Field(..., title="Время проведения пикника")
    city: CityBaseInDB = Field(..., title="Объект города")

    class Config:
        orm_mode: bool = True


class Picnics(BaseModel):
    id: int = Field(..., title="Идентификатор пикника")
    time: dt.datetime = Field(..., title="Время проведения пикника")
    users: Optional[List[PicnicRegistrationUsers]] = Field(..., title="Список пользователей на пикнике")
    city: CityBaseInDB = Field(..., title="Объект города")

    class Config:
        orm_mode: bool = True


class PicnicCreate(PicnicBase):
    pass


class PicnicRegister(BaseModel):
    user_id: int = Field(..., title="Идентификатор пользователя")


class PicnicRegisterResponse(BaseModel):
    id: int = Field(..., title="Идентификатор регистрации на пикник")
    picnic_id: int = Field(..., title="Идентификатор пикника")
    user: UserNameSurname = Field(..., title="Объект пользователя")

    class Config:
        orm_mode: bool = True
