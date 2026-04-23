from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class CreateReview(BaseModel):
    evaluation: int = Field(ge=1, le=5)
    images: str | None = None
    review_on_place: int
    desc: str | None = None


class ReviewResponse(CreateReview):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)