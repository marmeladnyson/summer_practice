
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import lifespan
from app.errors import AppError, app_error_handler
from app.routers import notes, users

app = FastAPI(lifespan=lifespan, exception_handlers={AppError: app_error_handler})

cors_origins = [origin.strip() for origin in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(notes.router)
app.include_router(users.router)


@app.get("/")
def lobby() -> str:
    return "Добро пожаловать в API заметок!"