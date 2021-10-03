from typing import Optional

from pydantic import BaseModel, Field


class CityBase(BaseModel):
    name: str = Field(..., title="Наименование города")


class CityBaseInDB(CityBase):
    class Config:
        orm_mode: bool = True


class City(CityBase):
    id: Optional[int] = Field(..., title="Идентификатор города")
    weather: Optional[str] = Field(..., title="Текущая температура в городе")

    class Config:
        orm_mode: bool = True


class CityCreate(CityBase):
    pass


class Cities(City):
    id: int = Field(..., title="Идентификатор города")
    weather: str = Field(..., title="Текущая температура в городе")
