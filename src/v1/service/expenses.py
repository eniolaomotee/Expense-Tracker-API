from fastapi import HTTPException,status
from sqlmodel import select, desc
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import func, extract
from src.v1.models.models import Expenses, ExpenseCategory
from src.v1.schemas.expenses import ExpenseCreate, ExpenseUpdate
import logging
import uuid
from sqlalchemy import cast, String
from typing import Optional
from datetime import date
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class ExpensesService:
    async def get_expense_by_uid(self,expense_uid:uuid.UUID, session:AsyncSession):
        "Get an expense by it's id"
        statement = select(Expenses).where(Expenses.uid == expense_uid)
        result = await session.exec(statement)
        expense = result.first()
        return expense
    
    async def create_expense(self,expense_items:ExpenseCreate,user_uid:uuid.UUID, session:AsyncSession):
        "Create expense items"
        expense = expense_items.model_dump()
        new_expense = Expenses(**expense, user_uid=user_uid)
        session.add(new_expense)
        await session.commit()
        await session.refresh(new_expense)
        return new_expense
    
    async def update_expense(self,expense_uid:uuid.UUID, expense_items:ExpenseUpdate, session:AsyncSession):
        "Get the expense to be updates"
        expense_to_update = await self.get_expense_by_uid(expense_uid=expense_uid, session=session)
        
        if not expense_to_update:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
        
        for key, value in expense_items.model_dump(exclude_unset=True).items():
            if key not in {"uid","created_at"}:
                setattr(expense_to_update,key,value)

        session.add(expense_to_update)
        await session.commit()
        await session.refresh(expense_to_update)
        
        return expense_to_update
                
                
    async def delete_expense(self, expense_uid:uuid.UUID, session:AsyncSession):
        "Delete an Expense by it's ID"
        expense_to_be_deleted = await self.get_expense_by_uid(expense_uid=expense_uid, session=session)
        
        if expense_to_be_deleted is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
        
        await session.delete(expense_to_be_deleted)
        await session.commit()
        
    async def get_user_all_expenses(self,user_uid:uuid.UUID, session:AsyncSession, page:int=1, limit:int=10):
        "Get a user list of all expenses"
        offset = (page - 1) * limit
        statement = select(Expenses).where(Expenses.user_uid == user_uid).offset(offset).limit(limit)
        result = await session.exec(statement)
        user_expenses = result.all()
        
        count_statement = select(func.count()).select_from(Expenses).where(Expenses.user_uid == user_uid)
        total_result = await session.exec(count_statement)
        total = total_result.one()
        
        return {
            "data": user_expenses,
            "page":page,
            "limit":limit,
            "total":total
        }
        
    async def search_expense(self, search_term:str, session:AsyncSession):
        "Search for expense by title or description"
        statement = select(Expenses).where(
            (Expenses.title.ilike(f"%{search_term}%")) |
            (Expenses.description.ilike(f"%{search_term}%")) |
            (cast(Expenses.category, String).ilike(f"%{search_term}%"))
        ).order_by(Expenses.created_at.desc())
        
        result = await session.exec(statement=statement)
        searched_expense = result.all()
        
        return searched_expense
    
    async def get_expenses_by_category(self, expense_category: ExpenseCategory, session:AsyncSession):
        statement = select(Expenses).where(Expenses.category == expense_category)
        result = await session.exec(statement)
        expense_by_category = result.all()
        
        return expense_by_category

    async def get_expense_summary_monthly(self, date:date, user_uid:uuid.UUID, session:AsyncSession):
        statement = select(Expenses.category, func.sum(Expenses.amount).label("total")).where(
            extract("year", Expenses.created_at)  == date.year,
            extract("month", Expenses.created_at) == date.month,
            Expenses.user_uid == user_uid
            ).group_by(Expenses.category)
            
        
        result = await session.exec(statement)
        summary = result.all()
        
        # Transform to seriazable
        summary_data = [{"category": category, "total":float(total)} for category, total in summary]
        
        return {
            "month": date.strftime("%B %Y"),
            "summary":summary_data
        }

    async def filter_user_expenses(self, user_uid:uuid.UUID,filter_by:Optional[str], start_date: Optional[str],end_date:Optional[str],session:AsyncSession):
        statement = select(Expenses).where(Expenses.user_uid == user_uid)
        
        now = datetime.utcnow()
        
        if filter_by == "past_week":
            statement = statement.where(Expenses.created_at >= now - timedelta(days=7))
        elif filter_by == "past_month":
            statement = statement.where(Expenses.created_at >= now - timedelta(days=30))
        elif filter_by == "last_3_months":
            statement == statement.where(Expenses.created_at >= now - timedelta(days=90))
        elif filter_by == "custom":
            if start_date and end_date:
                statement = statement.where(Expenses.created_at >= start_date , Expenses.created_at <= end_date)
            else:
                raise ValueError("Custom filter requires both start date and end date")
        
        statement = statement.order_by(Expenses.created_at.desc())
        result = await session.exec(statement)
        return result.all()