from sqlalchemy.orm import  Session
from fastapi import HTTPException, status
from repositories.userRepo import UserRepo
from security import hash_password, verify_password, create_access_token
from schemes.auth import LoginData, RegisterData, TokenResponse
from schemes.users import UserResponse, CreateUser

class AuthService:
    def __init__(self, db: Session):
        self.userRepo = UserRepo(db)

    def register(self, data: RegisterData):
        existing = self.userRepo.get_by_username(data.username)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        hashed = hash_password(data.password)
        user = self.userRepo.create_user_with_hashpass(data.username, hashed)
        return UserResponse.model_validate(user)


    def login(self, data: LoginData):
        user = self.userRepo.get_by_username(data.username)
        if not user or not verify_password(data.password, user.hashpass):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


        token = create_access_token(user.id)
        return TokenResponse(access_token=token)
