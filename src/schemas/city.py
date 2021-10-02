from typing import Optional

from pydantic import BaseModel


class CityBase(BaseModel):
    name: str


class City(CityBase):
    id: Optional[int] = None
    weather: Optional[str] = None

    class Config:
        orm_mode: bool = True


class CityCreate(CityBase):
    pass


class Cities(City):
    id: int
    weather: str
