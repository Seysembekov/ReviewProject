from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from services.authService import AuthService
from schemes.auth import TokenResponse, LoginData, RegisterData
from schemes.users import CreateUser, UserResponse
from api.dependencies import get_db_Session, get_redis_client, get_current_user
from repositories.userRepo import UserRepo

app = APIRouter(prefix='/auth', tags=['Auth'])

@app.post('/register')
def register(data: RegisterData, db: Session = Depends(get_db_Session)):
    return AuthService(db).register(data)

@app.post('/login')
def login(data: LoginData, db: Session = Depends(get_db_Session)):
    return AuthService(db).login(data)

@app.get('/me')
def get_me(db: Session = Depends(get_db_Session),
           current_user: int = Depends(get_current_user)):
    user = UserRepo(db).get_by_id(current_user)
    if not user:
        raise HTTPException(status_code=404)
    return UserResponse.model_validate(user)
