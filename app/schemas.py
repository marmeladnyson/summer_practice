from pydantic import BaseModel

class Note(BaseModel):
    id: str
    title: str
    status: bool

class CreateNote(BaseModel):
    title: str

class UpdateNote(BaseModel):
    title: str | None = None
    status: bool | None = None