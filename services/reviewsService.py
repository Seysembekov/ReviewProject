from repositories.placeRepo import PlaceRepo
from repositories.userRepo import UserRepo
from schemes.reviews import ReviewResponse, CreateReview
from repositories.reviewRepo import ReviewRepo
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from services.placeService import PlaceService


class ReviewService:
    def __init__(self, db: Session):
        self.review_repo = ReviewRepo(db)
        self.place_repo = PlaceRepo(db)
        self.user_repo = UserRepo(db)

    def get_by_place(self, place_id: int):
        place = self.place_repo.get_by_id(place_id)
        if not place:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        reviews = self.review_repo.get_by_place(place_id)
        if not reviews:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return [ReviewResponse.model_validate(r) for r in reviews]

    def get_all(self, offset: int = 0, limit: int =20):
        reviews = self.review_repo.get_all(offset, limit)
        if not reviews:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return [ReviewResponse.model_validate(r) for r in reviews]

    def get_by_user(self, user_id: int):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND)

        user_reviews = self.review_repo.get_by_user(user_id)
        if not user_reviews:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return [ReviewResponse.model_validate(r) for r in user_reviews]

    def create_review(self, data: CreateReview, user_id):
        existing = self.place_repo.get_by_id(data.review_on_place)
        if not existing:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        review = self.review_repo.create_review(data, user_id)
        return ReviewResponse.model_validate(review)




