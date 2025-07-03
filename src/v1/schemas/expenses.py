from pydantic import BaseModel, Field, ConfigDict
from typing import Optional,List
from datetime import datetime
from src.v1.models.models import ExpenseCategory


class ExpenseCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    amount: float
    category : ExpenseCategory = Field(description="Must be one of groceries, leisure, electronics, utilites, clothing, health, food or others")
    description: Optional[str]
    
class ExpenseUpdate(ExpenseCreate):
    updated_at: datetime
    
class ExpenseOutput(BaseModel):
    title: str
    amount: float
    category:ExpenseCategory
    description: Optional[str]
    created_at : datetime
    
class PaginatedExpenses(BaseModel):
    data: List[ExpenseOutput]
    page : int
    limit: int 
    total :int
    
class ExpenseCategorySummary(BaseModel):
    category: str
    total: float
    
class ExpenseMonthlySummary(BaseModel):
    month: str
    summary : List[ExpenseCategorySummary]