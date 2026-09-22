from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./notes.db")
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
LocalSession = sessionmaker(bind=engine, class_=Session)

class Base(DeclarativeBase):
    pass

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield