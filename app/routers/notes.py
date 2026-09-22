from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import NotesORM
from app.schemas import CreateNote, Note, UpdateNote

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("", response_model=list[Note])
def read_notes(db: Session = Depends(get_db)):
    notes = db.scalars(select(NotesORM)).all()
    return notes


@router.post("", status_code=status.HTTP_201_CREATED, response_model=Note)
def create_note(payload: CreateNote, db: Session = Depends(get_db)):
    note = NotesORM(title=payload.title, status=False)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


@router.patch("/{note_id}", response_model=Note)
def update_note(note_id: str, payload: UpdateNote, db: Session = Depends(get_db)):
    note = db.scalars(select(NotesORM).where(NotesORM.id == note_id)).one_or_none()
    if note is None:
        raise HTTPException(status_code=404, detail="Такой заметки не существует")

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
        raise HTTPException(status_code=404, detail="Такой заметки не существует")

    db.delete(note)
    db.commit()