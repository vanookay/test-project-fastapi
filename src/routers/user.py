from typing import Any

from fastapi import APIRouter, Query, HTTPException
from sqlalchemy import func

from src.db.database import SessionLocal
from src.models.user import User
from src.schemas.user import UserModel, RegisterUserRequest

router: Any = APIRouter(
    tags=["user"],
    responses={404: {"Description": "Not found"}},
)


@router.post('/users-list/', summary='')
def users_list(filter_by: str = Query(description="Фильтр (max_age, min_age)", default=None)):
    """
    Список пользователей
    """
    if filter_by:
        # Есть риск, что лежит большой массив данных, используется подзапрос
        if filter_by == 'max_age':
            sub_query = SessionLocal().query(func.max(User.age)).scalar_subquery()
        elif filter_by == 'min_age':
            sub_query = SessionLocal().query(func.min(User.age)).scalar_subquery()
        else:
            raise HTTPException(status_code=400, detail='Данный фильтр не определен')
        users = SessionLocal().query(User).filter(User.age == sub_query)
    else:
        users = SessionLocal().query(User).all()

    return [{
        'id': user.id,
        'name': user.name,
        'surname': user.surname,
        'age': user.age,
    } for user in users]


@router.post('/register-user/', summary='CreateUser', response_model=UserModel)
def register_user(user: RegisterUserRequest):
    """
    Регистрация пользователя
    """
    user_object = User(**user.dict())
    s = SessionLocal()
    s.add(user_object)
    s.commit()

    return UserModel.from_orm(user_object)
