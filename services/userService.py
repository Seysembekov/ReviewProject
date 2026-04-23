from schemes.users import UserResponse, CreateUser
from repositories.userRepo import UserRepo
from repositories.placeRepo import PlaceRepo
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

class UserService:
    def __init__(self, db: Session):
        self.user_repo = UserRepo(db)
        self.place_repo = PlaceRepo(db)

    def get_all(self, offset: int = 0, limit: int = 20):
        all_user = self.user_repo.get_all(offset, limit)
        if not all_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return [UserResponse.model_validate(u) for u in all_user]

    def get_by_id(self, user_id):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return UserResponse.model_validate(user)

    def get_by_username(self, username: str):
        user = self.user_repo.get_by_username(username)
        if not user:
            raise HTTPException(status_code = 404)
        return UserResponse.model_validate(user)

    def get_favorites(self, user_id: int):
        favorites = self.user_repo.get_favorites(user_id)
        if not favorites:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return favorites

    def add_favorite(self, user_id, place_id):
        favorite = self.user_repo.get_favorites(user_id)
        ids = [p.id for p in favorite]
        if place_id in ids:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        if not self.place_repo.get_by_id(place_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        self.user_repo.add_to_favorite(user_id, place_id)

    def remove_from_favorite(self, user_id, place_id):
        favorite = self.user_repo.get_favorites(user_id)
        ids = [p.id for p in favorite]
        if place_id not in ids:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        self.user_repo.remove_from_favorite(user_id, place_id)

    def create_user(self, data: CreateUser):
        user = self.user_repo.create_user(data)
        return UserResponse.model_validate(user)
