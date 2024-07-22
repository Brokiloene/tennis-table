from typing import Annotated

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from config.settings import DATABASE_URL

engine = create_engine(
    url=DATABASE_URL,
    echo=True,
    pool_size=5,
    max_overflow=10,
)

session_factory = sessionmaker(engine, expire_on_commit=False)

class BaseModel(DeclarativeBase):
    pass
