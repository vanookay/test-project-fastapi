from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    surname: str
    age: int


class User(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode: bool = True


class UserCreate(UserBase):
    pass


class Users(User):
    id: int
