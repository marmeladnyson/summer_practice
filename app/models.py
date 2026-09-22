from uuid import uuid4
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class NotesORM(Base):
    __tablename__ = "notes"
    
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    title: Mapped[str]
    status: Mapped[bool] = mapped_column(default=False)

class UsersORM(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    email: Mapped[str] = mapped_column(unique=True)
    phone: Mapped[str]