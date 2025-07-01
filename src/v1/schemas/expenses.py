from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from src.v1.models.models import ExpenseCategory


class ExpenseCreate(BaseModel):
    title: str
    amount: float
    category : ExpenseCategory
    description: Optional[str]
    created_at : datetime 
    updated_at : datetime 
    
