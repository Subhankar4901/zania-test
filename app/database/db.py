from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect,create_engine
import os
from models import Base
if os.getenv("db_env","test")=="prod":
    DATABASE_URI_ASYNC="postgresql+asyncpg://zania:zania@db:5432/prod"
    DATABASE_URI_SYNC="postgresql+psycopg2://zania:zania@db:5432/prod"
else:
    DATABASE_URI_ASYNC="postgresql+asyncpg://zania:zania@db:5432/test"
    DATABASE_URI_SYNC="postgresql+psycopg2://zania:zania@db:5432/test"

async_engine=create_async_engine(DATABASE_URI_ASYNC)
sync_engine=create_engine(DATABASE_URI_SYNC)
db_session=sessionmaker(bind=async_engine,class_=AsyncSession,expire_on_commit=False,autoflush=False)

# Get the database session for dependency injection
async def get_db():
    async with db_session() as session:
        yield session

# Initialize the database. It gets to run only once in start up.
async def init_db():
    required_tables = {"products", "oders", "oder_product"} # Don't touch the names
    inspector=inspect(sync_engine)
    existing_tables=inspector.get_table_names()
    if not required_tables.issubset(set(existing_tables)):
        print("Missing required tables. Reinitiallizing database.")
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
    else:
        print("All required tables are present. skipping initialization.")