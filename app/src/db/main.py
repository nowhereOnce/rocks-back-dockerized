from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import text, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from src.config import settings
from contextlib import asynccontextmanager

# async_engine: Asynchronous database engine that allows performing operations in PostgreSQL.
async_engine = create_async_engine(url=settings.POSTGRES_URL, echo=True)

# AsyncSessionLocal: Factory for asynchronous sessions
AsyncSessionLocal = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)

# init_db: Function responsible for creating the tables in the database using the model definitions.
async def init_db():
    """
    Initializes the database by creating all defined tables.
    
    This function uses SQLModel's metadata to create tables if they do not exist.
    It imports the models internally to ensure they are registered before creation.
    """
    async with async_engine.begin() as conn:
        from .models import Rocks, Locations, Samples, User

        await conn.run_sync(SQLModel.metadata.create_all)

# get_session: Function that provides asynchronous database sessions that can be used to perform operations on the database.
async def get_session() -> AsyncSession:
    """
    Dependency function that provides an asynchronous database session.
    
    Yields:
        AsyncSession: An asynchronous database session.
    """
    async with AsyncSessionLocal() as session:
        yield session
