import datetime as dt

from pydantic import BaseModel


class PicnicCreateRequest(BaseModel):
    city_id: int
    time: dt.datetime
