from typing import Any, List

from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src.schemas.city import Cities, CityCreate, City
from src.services.city import get_cities, city_create, get_by_name, check_existing
from src.services.general import get_db

router: Any = APIRouter(
    tags=["city"],
    responses={
        400: {"Description": "Неверные параметры запроса"},
        404: {"Description": "Не найдено"}
    },
)


@router.get('/city/', summary='Get Cities list', description='Получение списка городов', response_model=List[Cities])
def cities_list(
        db: Session = Depends(get_db),
        q: str = Query(description="Название города", default=None)
) -> List:
    """
    Получение списка городов с текущей температурой
    """

    return get_cities(db=db, q=q)


@router.post('/city/', summary='Create City', description='Создание города', response_model=City,
             status_code=status.HTTP_201_CREATED)
def create_city(city: CityCreate, db: Session = Depends(get_db)) -> Any:
    """
    Создание записи города
    """

    city_object = get_by_name(db, name=city.name)
    if city_object:
        raise HTTPException(
            status_code=400,
            detail="Город с таким названием уже существует в системе.",
        )
    if not check_existing(city.name):
        raise HTTPException(
            status_code=404,
            detail='Город с таким названием не найден.'
        )

    return city_create(db=db, city=city)
