from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: str
    phone: str


class CreateUser(BaseModel):
    email: str
    phone: str


class Note(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    status: bool
    user_id: str

class CreateNote(BaseModel):
    title: str
    user_id: str

class UpdateNote(BaseModel):
    title: str | None = None
    status: bool | None = None


class NotesPage(BaseModel):
    items: list[Note]
    skip: int
    limit: int
    total: int