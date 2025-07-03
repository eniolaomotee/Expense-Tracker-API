from fastapi import status, APIRouter, Depends, Query
from src.v1.schemas.expenses import ExpenseCreate, ExpenseOutput, PaginatedExpenses, ExpenseMonthlySummary
from src.v1.service.expenses import ExpensesService
from src.database.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime
import logging
from typing import Optional
import uuid
from src.core.dependencies import AccessTokenBearer
from src.v1.models.models import ExpenseCategory


logger = logging.getLogger(__name__)

expense_router = APIRouter()
expense_service = ExpensesService()
access_bearer_token= AccessTokenBearer()


@expense_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_expense(expense_items:ExpenseCreate, session:AsyncSession = Depends(get_session), token_details=Depends(access_bearer_token)):
    user_uid = uuid.UUID(token_details.get("user_data")["user_uid"])
    logger.debug("This is the users uid %s", user_uid)
    new_expense = await expense_service.create_expense(expense_items=expense_items, user_uid=user_uid, session=session)
    return new_expense
    
@expense_router.put("/{expense_uid}", response_model=ExpenseOutput)
async def update_expense(expense_data:ExpenseCreate, expense_uid:uuid.UUID, session:AsyncSession=Depends(get_session), token_details=Depends(access_bearer_token)):
    
    updated_expense = await expense_service.update_expense(expense_uid=expense_uid,expense_items=expense_data, session=session)
    
    return updated_expense


@expense_router.get("/search")
async def search_expenses(
    search_term: str = Query(min_length=1, max_length=100, description="Search keyword in title or description"),
    session:AsyncSession= Depends(get_session),
    token_details= Depends(access_bearer_token)
):
    search_expense = await expense_service.search_expense(search_term=search_term,session=session)
    
    return search_expense

@expense_router.get("/summary", status_code=status.HTTP_200_OK, response_model=ExpenseMonthlySummary)
async def get_expense_summary_monthly(date:datetime, session:AsyncSession=Depends(get_session), token_details=Depends(access_bearer_token)):
    user_uid = token_details.get("user_data")["user_uid"]
    logger.debug("This is the users uid %s", user_uid)
    
    summary_expense = await expense_service.get_expense_summary_monthly(date=date, user_uid=user_uid, session=session)
    
    return summary_expense

@expense_router.get("/filter")
async def get_filtered_response(
    user_uid:str,
    filter_by: Optional[str] = Query(None,enum=["past_week", "past_month", "last_3_months","custom"]),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    session: AsyncSession = Depends(get_session)):
    
    
    return await expense_service.filter_user_expenses(
        user_uid=user_uid,
        filter_by=filter_by,
        start_date=start_date,
        end_date=end_date,
        session=session
    )

@expense_router.get("/category/{by-category}", status_code=status.HTTP_200_OK)
async def get_expense_by_category(expense_category: ExpenseCategory, session:AsyncSession=Depends(get_session), token_details=Depends(access_bearer_token)):
    expense_by_category = await expense_service.get_expenses_by_category(expense_category=expense_category,session=session)
    return expense_by_category



@expense_router.get("/{expense_uid}", status_code=status.HTTP_200_OK)
async def get_expense_by_id(expense_uid:uuid.UUID, session:AsyncSession = Depends(get_session), token_details=Depends(access_bearer_token)):
    expense = await expense_service.get_expense_by_uid(expense_uid=expense_uid, session=session)
    return expense

@expense_router.delete("/{expense_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(expense_uid:uuid.UUID,session:AsyncSession=Depends(get_session)):
    await expense_service.delete_expense(expense_uid=expense_uid, session=session)
    
    return {"detail": "Expense Deleted Successfully."}

@expense_router.get("/", response_model=PaginatedExpenses)
async def get_all_user_expenses(token_details=Depends(access_bearer_token), page: int = 1,limit: int = 10, session:AsyncSession=Depends(get_session)):
    user_uid = uuid.UUID(token_details.get("user_data")["user_uid"])
    all_expenses = await expense_service.get_user_all_expenses(user_uid=user_uid, page=page,limit=limit,session=session)
    return all_expenses    


