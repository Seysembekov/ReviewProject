from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

class CreatePlace(BaseModel):
    name: str
    address: str
    media: str | None

class PlaceResponse(CreatePlace):
    id: int

    model_config = ConfigDict(from_attributes=True)