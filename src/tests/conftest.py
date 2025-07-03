from typing import AsyncGenerator
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from src.database.main import get_session
from src import app
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from src.utils.config import settings
from sqlmodel import SQLModel,select
from src.v1.models.models import User
# Used SQLite for tests
TEST_DATABASE_URL = settings.DATABASE_URL_TEST


test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    connect_args= {"check_same_thread": False}
)

TestSessionLocal = async_sessionmaker(bind=test_engine, class_=AsyncSession, expire_on_commit=False,autoflush=False)

async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestSessionLocal() as session:
        yield session

app.dependency_overrides[get_session] = override_get_session


# TEST DB schema
@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    await test_engine.dispose()

@pytest_asyncio.fixture()
async def async_client() -> AsyncGenerator[AsyncClient,None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

@pytest_asyncio.fixture(autouse=True)
async def clear_tables():
    async with TestSessionLocal() as session:
        for table in reversed(SQLModel.metadata.sorted_tables):
            await session.exec(table.delete())
        await session.commit()
        
@pytest_asyncio.fixture()
async def confirmed_user(async_client:AsyncClient):
    user_data = {
        "email": "test@example.com",
        "password": "12345"
    }
    
    response = await async_client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 201, f"User registeration failed, {response.text}"
    
    async with TestSessionLocal() as session:
        statement = select(User).where(User.email == user_data.get("email"))
        result = await session.exec(statement)
        user = result.first()
        assert user , "User found in the Db"
        user_data["uid"] = user.uid
        
    return user_data


@pytest_asyncio.fixture()
async def logged_in_token(async_client:AsyncClient, confirmed_user:dict):
    response = await async_client.post(
        url="/api/v1/auth/login",
        json={
            "email": confirmed_user["email"],
            "password": confirmed_user["password"]
        }
    )
    
    assert response.status_code == 200, f"Failed to log in {response.text}"
    return response.json().get("tokens")["access_token"]
    
