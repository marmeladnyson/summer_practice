from uuid import uuid4
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class NotesORM(Base):
    __tablename__ = "notes"
    
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    title: Mapped[str]
    status: Mapped[bool] = mapped_column(default=False)

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["UsersORM"] = relationship(back_populates="notes")

class UsersORM(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    email: Mapped[str] = mapped_column(unique=True)
    phone: Mapped[str]

    notes: Mapped[list["NotesORM"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )