from contextlib import asynccontextmanager
from uuid import uuid4
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Mapped, Session, mapped_column, sessionmaker, DeclarativeBase
from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import BaseModel


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(lifespan=lifespan)

DATABASE_URL = "postgresql+psycopg2://postgres:admin@localhost:6767/summer_practice_code"
engine = create_engine(DATABASE_URL)
LocalSession = sessionmaker(bind=engine, class_=Session)

# ORM модели
class Base(DeclarativeBase):
    pass

class NotesORM(Base):
    __tablename__ = "notes"
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    title: Mapped[str]
    status: Mapped[bool] = mapped_column(default=False)

# Pydantic модели
class Notes(BaseModel):
    id: str
    title: str
    status: bool

class CreateNotes(BaseModel):
    title: str

class UpdateNotes(BaseModel):
    title: str | None = None
    status: bool | None = None

# CRUD API
@app.get("/")
def lobby() -> str:
    return "Добро пожаловать в API заметок!"
    

@app.get("/notes")
def read_notes(db: Session = Depends(get_db)) -> list[Notes]:
    notes = db.scalars(select(NotesORM)).all()
    return [Notes(id=note.id, title=note.title, status=note.status) for note in notes]

@app.post("/notes", status_code=status.HTTP_201_CREATED)
def create_notes(payload: CreateNotes, db: Session = Depends(get_db)) -> Notes:
    note = NotesORM(id=str(uuid4()), title=payload.title, status=False)
    
    db.add(note)
    db.commit()
    db.refresh(note)
    
    return Notes(id=note.id, title=note.title, status=note.status)

@app.patch("/notes")
def update_notes(note_id: str, payload: UpdateNotes, db: Session = Depends(get_db)) -> Notes:
    note = db.scalars(select(NotesORM).where(NotesORM.id == note_id)).one_or_none()
    if note is None:
        raise HTTPException(status_code=404, detail="Такой заметки не существует")
    if note.title is not None:
        note.title = payload.title
    if note.status is not None:
        note.status = payload.status

    db.commit()
    db.refresh(note)

    return Notes(id=note.id, title=note.title, status=note.status)

@app.delete("/notes")
def delete_notes(note_id: str, db: Session = Depends(get_db)) -> None:
    note = db.scalars(select(NotesORM).where(NotesORM.id == note_id)).one_or_none()
    if note is None:
        raise HTTPException(status_code=404, detail="Такой заметки не существует")
    
    db.delete(note)
    db.commit()
    db.refresh(note)

