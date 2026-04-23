from sqlalchemy.orm import Session
from database import get_db
from redis_client import get_redis
from fastapi import Depends, HTTPException, status
import redis.asyncio as aioredis
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from security import decode_token


def get_db_Session(db: Session = Depends(get_db)):
    return db

async def get_redis_client(redis=Depends(get_redis)):
    return redis

bearer_scheme = HTTPBearer()

async def get_current_user(
        credentials: HTTPAuthorizationCredentials=Depends(bearer_scheme),
        db: Session = Depends(get_db_Session)):
         try:
             user_id = decode_token(credentials.credentials)
             return user_id
         except JWTError:
             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, headers={'WWW-Authenticate': 'Bearer'})