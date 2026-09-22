


from fastapi import FastAPI

from app.database import lifespan
from app.routers import notes

app = FastAPI(lifespan=lifespan)

app.include_router(notes.router)


@app.get("/")
def lobby() -> str:
    return "Добро пожаловать в API заметок!"