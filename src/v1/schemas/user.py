from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):    
    email: EmailStr
    password: str
    
class UserOutput(BaseModel):
    email:EmailStr
    is_active:bool 
    created_at: datetime
    