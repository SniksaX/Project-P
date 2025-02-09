# database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+asyncpg://your_user:your_password@localhost/your_dbname"

# Create the async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a configured "async session" class
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False)

# Base class for declarative models
Base = declarative_base()
