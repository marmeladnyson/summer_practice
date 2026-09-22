from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.errors import NoteNotFoundError, UserNotFoundError
from app.models import NotesORM, UsersORM
from app.schemas import CreateNote, Note, NotesPage, UpdateNote

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("", response_model=NotesPage)
def read_notes(
    status_filter: bool | None = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    if skip < 0 or not 1 <= limit <= 100:
        raise HTTPException(status_code=400, detail="skip должен быть >= 0, limit от 1 до 100")

    query = select(NotesORM)
    count_query = select(func.count()).select_from(NotesORM)
    if status_filter is not None:
        query = query.where(NotesORM.status == status_filter)
        count_query = count_query.where(NotesORM.status == status_filter)

    notes = db.scalars(query.offset(skip).limit(limit)).all()
    return NotesPage(items=notes, skip=skip, limit=limit, total=db.scalar(count_query) or 0)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=Note)
def create_note(payload: CreateNote, db: Session = Depends(get_db)):
    user = db.get(UsersORM, payload.user_id)
    if user is None:
        raise UserNotFoundError(payload.user_id)

    note = NotesORM(title=payload.title, status=False, user_id=payload.user_id)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


@router.patch("/{note_id}", response_model=Note)
def update_note(note_id: str, payload: UpdateNote, db: Session = Depends(get_db)):
    note = db.scalars(select(NotesORM).where(NotesORM.id == note_id)).one_or_none()
    if note is None:
        raise NoteNotFoundError(note_id)

    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(note, key, value)

    db.commit()
    db.refresh(note)
    return note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: str, db: Session = Depends(get_db)):
    note = db.scalars(select(NotesORM).where(NotesORM.id == note_id)).one_or_none()
    if note is None:
        raise NoteNotFoundError(note_id)

    db.delete(note)
    db.commit()