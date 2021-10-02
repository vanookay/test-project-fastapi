from typing import Any

from fastapi import APIRouter

from src.api.api_v1.routers import city, picnic, user

v1_routers: Any = APIRouter(prefix='/v1')

v1_routers.include_router(city.router)
v1_routers.include_router(picnic.router)
v1_routers.include_router(user.router)
