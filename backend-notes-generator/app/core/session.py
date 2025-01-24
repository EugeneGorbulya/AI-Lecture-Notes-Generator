from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core import config

DATABASE_URL = config.settings.DATABASE_URL
engine = create_async_engine(DATABASE_URL, future=True, echo=True)

async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)