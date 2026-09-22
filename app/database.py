from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session

DATABASE_URL = "postgresql+psycopg2://postgres:admin@localhost:6767/summer_practice_code"

engine = create_engine(DATABASE_URL)
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