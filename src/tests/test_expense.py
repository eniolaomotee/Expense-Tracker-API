import pytest
from httpx import AsyncClient
from fastapi import status

async def created_expense(expense_uid:str, async_client:AsyncClient, logged_in_token:str):
    headers = {"Authorization": f"Bearer {logged_in_token}"}
    response = await async_client.get(
        url=f"/api/v1/expense/{expense_uid}",
        headers=headers
    )
    
    return response.json()

@pytest.mark.asyncio
async def test_create_expense(async_client: AsyncClient, logged_in_token:str,confirmed_user:dict):
    headers= {"Authorization": f"Bearer {logged_in_token}"}
    response = await async_client.post(
        url="/api/v1/expense/",
        json={
            "title": "Buy Mom a cloth for her birthday",
            "amount": 20.00,
            "category":"clothing",
            "description":"Getting mummy a cloth as a gift"
        },headers=headers)
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["title"] == "Buy Mom a cloth for her birthday"
    
    
@pytest.mark.asyncio
async def test_create_expense_without_token(async_client:AsyncClient):
    response = await async_client.post(
        url="/api/v1/expense/",
        json={
            "title": "Buy Mom a cloth for her birthday",
            "amount": 20.00,
            "category":"clothing",
            "description":"Getting mummy a cloth as a gift"
        })
    
    
    assert response.status_code == status.HTTP_403_FORBIDDEN
    
    
@pytest.mark.asyncio
async def test_create_expense_without_body(async_client:AsyncClient, logged_in_token: str):
    headers = {"Authorization": f"Bearer {logged_in_token}"}
    response = await async_client.post(
        url="/api/v1/expense/",
        json={},
        headers=headers
    )
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

@pytest.mark.asyncio
async def test_get_expense(async_client:AsyncClient, logged_in_token:str):
    headers = {"Authorization": f"Bearer {logged_in_token}"}
    response = await async_client.get(
        url="/api/v1/expense/",
        headers=headers
    )
    
    assert response.status_code == status.HTTP_200_OK
    assert {"data":[], "page": 1, "limit":10, "total":0}.items() <= response.json().items()
    
@pytest.mark.asyncio
async def test_search_term(async_client:AsyncClient, logged_in_token:str):
    headers = {"Authorization": f"Bearer {logged_in_token}"}
    search_term = "Mom"
    response = await async_client.get(
        url=f"/api/v1/expense/search?search_term={search_term}",
        headers=headers
    )
    
    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(data, list)
    
@pytest.mark.asyncio
async def test_get_todo_by_id(async_client:AsyncClient, logged_in_token:str):
    headers = {"Authorization": f"Bearer {logged_in_token}"}
    response = await async_client.post(
        url="/api/v1/expense/",
        json={
            "title": "Buy Mom a cloth for her birthday",
            "amount": 20.00,
            "category":"clothing",
            "description":"Getting mummy a cloth as a gift"
        },
        headers=headers
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    expense_data = response.json()
    expense_uid = expense_data["uid"]
    
    # Using helper function
    get_response = await created_expense(expense_uid=expense_uid, async_client=async_client, logged_in_token=logged_in_token)
    
    data = get_response
    assert data["uid"] == expense_uid
    assert data["title"] == "Buy Mom a cloth for her birthday"
    
