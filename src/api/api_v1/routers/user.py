from typing import Any, List, Optional

from fastapi import APIRouter, Query, Depends, status
from sqlalchemy.orm import Session

from src.schemas.user import Users, UserCreate, User
from src.services.general import get_db
from src.services.users import create_user, get_users

router: Any = APIRouter(tags=["users"])


@router.get('/users/', summary='Get users list', response_model=List[Users])
def users_list(
        db: Session = Depends(get_db),
        min_age: Optional[int] = Query(description="Минимальный возраст", default=None, ge=0),
        max_age: Optional[int] = Query(description="Максимальный возраст", default=None, le=150)
) -> List:
    """
    Получение списка пользователей
    """

    return get_users(db=db, min_age=min_age, max_age=max_age)


@router.post('/users/', summary='Create a user', response_model=User, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)) -> Any:
    """
    Регистрация пользователя
    """

    return create_user(db=db, user=user)
