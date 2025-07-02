import logging
from datetime import datetime, timedelta
import uuid
from jose import jwt
from passlib.context import CryptContext
from src.utils.config import settings

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    logger.debug("Verifying Password")
    return pwd_context.verify(plain_password,hashed_password)

def hash_password(plain_password):
    logger.debug("password Hash")
    return pwd_context.hash(plain_password)

def create_access_token(user_data:dict, refresh:bool = False):
    expire_minutes = (settings.REFRESH_TOKEN_EXPIRE_MINUTES if refresh else settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "user_data": user_data,
        "exp": datetime.utcnow() + timedelta(minutes=expire_minutes),
        "jti": str(uuid.uuid4()),
        "refresh": refresh
    }
    
    token = jwt.encode(payload, settings.SECRET_KEY, settings.ALGORITHM)
    return token

def decode_access_token(token:str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.PyJWTError as e:
        logging.error(f"Token decoding failed: {e}")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occured: {e}")
        return None