from fastapi import status
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio()
async def test_register_user_success(async_client:AsyncClient):
    user_data = {"email":"test@test.com", "password":"12345"}
    response = await async_client.post(
        url="/api/v1/auth/register",
        json=user_data
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["email"] == user_data["email"]


@pytest.mark.asyncio()
async def test_register_duplicate_user(async_client:AsyncClient,confirmed_user):
    response = await async_client.post(
        url="/api/v1/auth/register",
        json=confirmed_user["email"]
    )
    
    response.status_code == status.HTTP_403_FORBIDDEN
    response.json()["detail"] == "User already exists"

@pytest.mark.asyncio()
async def test_register_invalid_inputs(async_client:AsyncClient, email="invalidemail",password="12345"):
    response = await async_client.post(
        url="/api/v1/auth/register",
        json={
            "email": email,
            "password":password
        }
    )
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

@pytest.mark.asyncio()
async def test_login_user_success(async_client:AsyncClient,confirmed_user):
    response = await async_client.post(
        url="/api/v1/auth/login",
        json={"email":confirmed_user["email"], "password":confirmed_user["password"]}
    )
    
    assert response.status_code == status.HTTP_200_OK
    assert "tokens" in response.json()


@pytest.mark.asyncio()
async def test_invalid_credentials(async_client:AsyncClient):
    response = await async_client.post(
        url="/api/v1/auth/login",
        json={"email":"nonexistent@test.com", "password":"29283802"}
    )    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
