import pytest
from httpx import AsyncClient
from fastapi import status



@pytest.mark.asyncio
async def test_create_expense(async_client: AsyncClient, logged_in_token:str,confirmed_user:dict):
    headers= {"Authorization": f"Bearer {logged_in_token}"}
    response = await async_client.post(
        url="/api/v1/expense/",
        json={
            "title": "Buy Mom a cloth for her birthday",
            "amount": 20.00,
            "category":"clothing",
            "description":"Getting mummy a cloth as a gift",
            "user_uid":confirmed_user["uid"]

        },headers=headers)
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["title"] == "Buy Mom a cloth for her birthday"
    
    
# @pytest.mark.asyncio
# async def test_create_todo_without_token(async_client:AsyncClient):
#     response = await async_client.post(
#         url="/api/v1/todo/",
#         json={
#             "title":"Buy Plantains",
#             "description":"From iya loja"
#         }
#     )
    
#     assert response.status_code == status.HTTP_403_FORBIDDEN
    
    
# @pytest.mark.asyncio
# async def test_create_todo_without_body(async_client:AsyncClient, logged_in_token: str):
#     headers = {"Authorization": f"Bearer {logged_in_token}"}
#     response = await async_client.post(
#         url="/api/v1/todo/",
#         json={},
#         headers=headers
#     )
    
#     assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

# @pytest.mark.asyncio
# async def test_get_todo(async_client:AsyncClient, logged_in_token:str):
#     headers = {"Authorization": f"Bearer {logged_in_token}"}
#     response = await async_client.get(
#         url="/api/v1/todo/",
#         headers=headers
#     )
    
#     assert response.status_code == status.HTTP_200_OK
#     assert {"data":[], "page": 1, "limit":10, "total":0}.items() <= response.json().items()
    
# @pytest.mark.asyncio
# async def test_search_term(async_client:AsyncClient, logged_in_token:str):
#     headers = {"Authorization": f"Bearer {logged_in_token}"}
#     search_term = "Buy"
#     response = await async_client.get(
#         url=f"/api/v1/todo/search?search_term={search_term}",
#         headers=headers
#     )
    
#     data = response.json()
#     assert response.status_code == status.HTTP_200_OK
#     assert isinstance(data, list)
    
# @pytest.mark.asyncio
# async def test_get_todo_by_id(async_client:AsyncClient, logged_in_token:str):
#     headers = {"Authorization": f"Bearer {logged_in_token}"}
#     response = await async_client.post(
#         url="/api/v1/todo/",
#         json={
#             "title": "Test Todo UID",
#             "description":"This is a test todo based on it's uuid"
#         },
#         headers=headers
#     )
    
#     assert response.status_code == status.HTTP_201_CREATED
#     todo_data = response.json()
#     todo_uid = todo_data["todo_uid"]
    
#     # Using helper function
#     get_response = await created_todo(todo_uid=todo_uid, async_client=async_client, logged_in_token=logged_in_token)
    
#     data = get_response
#     assert data["todo_uid"] == todo_uid
#     assert data["title"] == "Test Todo UID"
    
