from schemes.places import PlaceResponse, CreatePlace
from repositories.placeRepo import PlaceRepo
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

class PlaceService:
    def __init__(self, db: Session):
        self.place_repo = PlaceRepo(db)

    def get_all(self, offset: int = 0, limit: int = 20):
        places = self.place_repo.get_all(offset, limit  )
        if not places:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
        return [PlaceResponse.model_validate(p) for p in places]

    def get_by_id(self, place_id: int):
        place = self.place_repo.get_by_id(place_id)
        if not place:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return PlaceResponse.model_validate(place)

    def create_place(self, data: CreatePlace):
        place = self.place_repo.create_place(data)
        return PlaceResponse.model_validate(place)