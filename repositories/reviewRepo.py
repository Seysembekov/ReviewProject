from sqlalchemy.orm import Session
from models.reviews import Reviews
from schemes.reviews import CreateReview


class ReviewRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_by_place(self, place_id: int):
        return self.db.query(Reviews).filter(Reviews.review_on_place == place_id).all()

    def get_all(self, offset: int = 0, limit: int = 20):
        return self.db.query(Reviews).offset(offset).limit(limit).all()

    def get_by_user(self, user_id: int):
        return (
            self.db.query(Reviews)
            .filter(Reviews.user_id == user_id)
            .order_by(Reviews.created_at.desc())
            .all()
        )

    def create_review(self, data: CreateReview, user_id: int):
        review = Reviews(**data.model_dump(), user_id=user_id)
        self.db.add(review)
        self.db.commit()
        self.db.refresh(review)
        return review