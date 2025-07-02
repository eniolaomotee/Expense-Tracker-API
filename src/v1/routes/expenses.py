from fastapi import status, APIRouter, Depends, Query
from src.v1.schemas.expenses import ExpenseCreate
from src.v1.service.expenses import ExpensesService
from src.database.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime
import logging
from typing import Optional


logger = logging.getLogger(__name__)

expense_router = APIRouter()
expense_service = ExpensesService()

@expense_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_expense(expense_items:ExpenseCreate, session:AsyncSession = Depends(get_session)):
    pass








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