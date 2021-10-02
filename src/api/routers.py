from fastapi import APIRouter

from src.api.api_v1.api_routers import v1_routers

api_router = APIRouter(prefix='/api')

api_router.include_router(v1_routers)
