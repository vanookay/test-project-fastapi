from typing import Optional

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    name: str = Field(..., title="Имя пользователя")
    surname: str = Field(..., title="Фамилия пользователя")
    age: int = Field(..., title="Возраст пользователя")


class User(UserBase):
    id: Optional[int] = Field(..., title="Идентификатор пользователя")

    class Config:
        orm_mode: bool = True


class UserNameSurname(BaseModel):
    name: str = Field(..., title="Имя пользователя")
    surname: str = Field(..., title="Фамилия пользователя")

    class Config:
        orm_mode: bool = True


class UserCreate(UserBase):
    pass


class Users(User):
    id: int = Field(..., title="Идентификатор пользователя")
