from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from config import settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str):
    return pwd_context.verify(plain, hashed)

def create_access_token(user_id: int):
    payload = {'user_id': user_id,
               'exp': datetime.utcnow() + timedelta(minutes=settings.TOKEN_EXPIRE)}

    return jwt.encode(payload, settings.SECRET_KEY, algorithm= 'HS256')

def decode_token(token: str):
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

    user_id = payload.get('user_id')
    if not user_id:
        raise JWTError('user_id not found in token')
    return user_id