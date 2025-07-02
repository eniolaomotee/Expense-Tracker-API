import logging
from abc import ABC, abstractmethod
from fastapi import Depends,Request, status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from sqlmodel.ext.asyncio.session import AsyncSession
from src.database.main import get_session
from src.utils.security import decode_access_token
from src.v1.service.auth import AuthService

logger = logging.getLogger(__name__)


auth_service = AuthService()

class TokenBearer(HTTPBearer,ABC):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)
        
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        credentials = await super().__call__(request)
        
        token = credentials.credentials
        logger.debug("token from bearer auth %s", token)
        token_data = decode_access_token(token=token)
        logger.debug("token data from token %s", token_data)
        
        if token_data is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Authentication credentials"
            )
        
        self.verify_token_data(token_data)
        
        return token_data
    
    @abstractmethod
    def verify_token_data(self, token_data:dict) -> None:
        pass
    
class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data.get("refresh", False):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an Access Token, not a Refresh Token"
            )
            
class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data.get("refresh", False):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide a Refresh Token, not an Access Token"
            )
            

async def get_current_user(token:str=Depends(AccessTokenBearer()), session:AsyncSession = Depends(get_session)):
    user_email = token["user_data"]["email"]
    logger.debug("This is the users email %s", user_email)
    user = await auth_service.get_user_by_email(email=user_email, session=session)
    return user