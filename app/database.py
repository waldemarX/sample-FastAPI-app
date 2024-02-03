from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import (
    SQLAlchemyUserDatabase,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from auth.models import User
from base_class import Base
from config import DB_PASSWORD, DB_USERNAME


DATABASE_URL = (
    f"postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@localhost/test"
)


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)