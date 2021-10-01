from typing import Any

from fastapi import APIRouter

from src.db.database import SessionLocal
from src.models.user import User
from src.schemas.user import UserModel, RegisterUserRequest

router: Any = APIRouter(
    tags=["user"],
    responses={404: {"Description": "Not found"}},
)


@router.post('/users-list/', summary='')
def users_list():
    """
    Список пользователей
    """
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
