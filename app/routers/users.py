from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.errors import DatabaseConflictError
from app.models import UsersORM
from app.schemas import CreateUser, User

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[User])
def read_users(db: Session = Depends(get_db)):
    return db.scalars(select(UsersORM)).all()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=User)
def create_user(payload: CreateUser, db: Session = Depends(get_db)):
    existing_user = db.scalar(select(UsersORM).where(UsersORM.email == payload.email))
    if existing_user is not None:
        raise DatabaseConflictError("Пользователь с таким email уже существует")

    user = UsersORM(email=payload.email, phone=payload.phone)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user