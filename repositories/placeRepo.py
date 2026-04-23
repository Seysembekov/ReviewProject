from sqlalchemy.orm import Session
from models.places import Places
from schemes.places import CreatePlace


class PlaceRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, offset: int = 0, limit: int = 20):
        return self.db.query(Places).offset(offset).limit(limit).all()

    def get_by_id(self, place_id: int):
        return self.db.query(Places).filter(Places.id == place_id).first()

    def create_place(self, data: CreatePlace):
        place = Places(**data.model_dump())
        self.db.add(place)
        self.db.commit()
        self.db.refresh(place)
        return place
