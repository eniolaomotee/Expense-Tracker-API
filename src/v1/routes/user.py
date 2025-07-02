from fastapi import APIRouter, Depends, status,HTTPException
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from src.v1.schemas.user import UserCreate, UserOutput
from src.v1.service.auth import AuthService
from src.database.main import get_session
from src.utils.security import create_access_token, verify_password
import logging

logger = logging.getLogger(__name__)

auth_service = AuthService()
user_router = APIRouter()

@user_router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserOutput)
async def create_new_user(user_data:UserCreate, session:AsyncSession=Depends(get_session)):
    user_email = user_data.email
    user_exists = await auth_service.user_exist(email=user_email, session=session)
    
    if user_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User with this email already exists")
    
    user = await auth_service.create_user(user_details=user_data, session=session)
    
    return user
    

@user_router.post("/login")
async def login_user(user_login:UserCreate, session:AsyncSession=Depends(get_session)):
   user_email = user_login.email
   user_password = user_login.password
   
   user = await auth_service.get_user_by_email(email=user_email, session=session)
   
   if not user:
       raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
   
   password_valid = verify_password(user_password, user.password)
   
   if not password_valid:
       raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
   
   access_token = create_access_token(user_data={"email":user.email, "user_uid":str(user.uid)})
   refresh_token = create_access_token(user_data={"email":user.email, "user_uid":str(user.uid)}, refresh=True)
   
   
   return JSONResponse(
       content={
           "message": "Login Successful",
           "tokens": {
               "access_token": access_token,
               "refresh_token": refresh_token
           },
            "user": {"email":user.email, "user_uid":user.uid}
       },
       status_code=status.HTTP_200_OK
   )