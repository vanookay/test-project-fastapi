from typing import Optional

from sqlalchemy.orm import Session

from src.models.user import User
from src.schemas.user import UserCreate


def get_by_id(db: Session, user_id: int):
    """Получение пользователя по идентификатору из БД

    Args:
        db: Сессия БД
        user_id: Идентификатор пользователя

    Returns:
        Query пользователя

    """

    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session, min_age: Optional[int], max_age: Optional[int]) -> list:
    users = db.query(User)
    if min_age:
        users = users.filter(User.age >= min_age)
    if max_age:
        users = users.filter(User.age <= max_age)
    return users.all()


def create_user(db: Session, user: UserCreate):
    user_data = user.dict()
    user_post = User(**user_data)
    db.add(user_post)
    db.commit()
    db.refresh(user_post)
    return user_post
