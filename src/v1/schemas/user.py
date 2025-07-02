from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):    
    email: EmailStr
    password: str
    is_active: bool = False
    created_at: datetime 
    
    
class UserOutput(BaseModel):
    email:EmailStr
    is_active:bool 
    created_at: datetime
    