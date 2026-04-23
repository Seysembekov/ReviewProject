from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict



class CreateUser(BaseModel):
    username: str
    hashpass: str
    # reviews: list[int]


class UserResponse(BaseModel):
    id: int
    username: str
    # selected: bool = None
    model_config = ConfigDict(from_attributes=True)

