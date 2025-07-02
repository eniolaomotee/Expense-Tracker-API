from fastapi import HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.v1.models.models import User
from src.v1.schemas.user import UserCreate
from src.utils.security import hash_password
import logging


logger = logging.getLogger(__name__)

class AuthService:
    async def get_user_by_email(self,email:str,session:AsyncSession):
        logger.debug("Getting user by email from db")
        statement = select(User).where(User.email == email)
        result = await session.exec(statement=statement)
        user = result.first()
        return user
    
    async def user_exist(self, email:str,session:AsyncSession):

        user_exist = await self.get_user_by_email(email=email, session=session)
        logger.debug("Checking if the user exists %s", user_exist)
        
        return True if user_exist else False
    
    async def create_user(self, user_details:UserCreate, session:AsyncSession):
        user_email = user_details.email
        
        user_exists = await self.user_exist(email=user_email, session=session)
        
        if user_exists:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User already exists")
        
        hashed_password = hash_password(user_details.password)
        
        new_user = User(email=user_email, password=hashed_password, is_active=user_details.is_active)
        
        session.add(new_user)
        await session.commit(new_user)
        await session.refresh(new_user)
        return new_user
        
        
       