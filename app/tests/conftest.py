import pytest
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession
from sqlalchemy.orm import sessionmaker
from models import Base
TEST_DATABASE_URI="postgresql+asyncpg://zania:zania@db:5432/test"
async def _test_db_session():
    engine=create_async_engine(TEST_DATABASE_URI)
    db_session=sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with db_session() as session:
        yield session
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
