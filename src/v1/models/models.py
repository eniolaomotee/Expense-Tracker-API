import uuid
from datetime import datetime
from typing import Optional
from sqlmodel import Column, Field, Relationship, SQLModel
import sqlalchemy.dialects.postgresql as pg
import logging
from enum import Enum

logger = logging.getLogger(__name__)

class User(SQLModel, table=True):
    __tablename__ = "users"
    "Reps a user in the system"
    
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID, 
            primary_key=True, 
            unique=True, 
            nullable=False, 
            default=uuid.uuid4
        )
    )
    
    email: str
    password: str
    is_active: bool = False
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    
    
    def __repr__(self) -> str:
        logger.info("Repr of user Object")
        return f"User(uid={self.uid}, email={self.email}, is_active={self.is_active})"

class ExpenseCategory(str, Enum):
    GROCERIES = "groceries"
    LEISURE = "leisure"
    ELECTRONICS = "electronics"
    UTILITIES = "utilites"
    CLOTHING = "clothing"
    HEALTH = "health"
    FOOD = "food"
    OTHERS = "others"
 

class Expenses(SQLModel, table=True):
    __tablename__ = "expenses"
    
    uid : uuid.UUID = Field(default_factory=uuid.uuid4,sa_column=Column(pg.UUID, primary_key=True, nullable=False, index=True))
    title: str
    amount: float = Field(nullable=False)
    category : ExpenseCategory = Field(nullable=False)
    description: Optional[str]
    created_at : datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at : datetime = Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
    
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")