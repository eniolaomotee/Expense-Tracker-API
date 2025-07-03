from src.utils.config import settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
import logging
from typing import AsyncGenerator

logger = logging.getLogger(__name__)

engine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=False,
    future=True,
    connect_args= {"statement_cache_size":0}
)

AsyncSessionFactory = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    "Dependency for getting a DB session"
    async with AsyncSessionFactory() as session:
        try:
            yield session
            logger.debug("session %s", session)
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()
            
async def init_db():
    "Initialize the database by creating all tables"
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
        
async def close_db():
    "Close the Database connection"
    await engine.dispose()