from sqlalchemy.orm import Session
from models.users import Users
from models.places import Places
from models.favorites import Favorites
from schemes.users import CreateUser


class UserRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, offset: int = 0, limit: int = 20):
        return self.db.query(Users).offset(offset).limit(limit).all()

    def get_by_id(self, user_id: int):
        return self.db.query(Users).filter(Users.id == user_id).first()

    def get_by_username(self, username: str):
        return self.db.query(Users).filter(Users.username == username).first()

    def get_favorites(self, user_id: int):
        return (
            self.db.query(Places)
            .join(Favorites, Favorites.place_id == Places.id)
            .filter(Favorites.user_id == user_id)
            .all()
        )

    def add_to_favorite(self, user_id: int, place_id: int):
        fav = Favorites(user_id=user_id, place_id=place_id)
        self.db.add(fav)
        self.db.commit()

    def remove_from_favorite(self, user_id: int, place_id: int):
        self.db.query(Favorites).filter(
            Favorites.user_id == user_id,
            Favorites.place_id == place_id
        ).delete()
        self.db.commit()

    def create_user_with_hashpass(self, username: str, hashed_pass: str):
        user = Users(username=username, hashpass = hashed_pass)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def create_user(self, data: CreateUser):
        user = Users(username=data.username, hashpass=data.hashpass)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
