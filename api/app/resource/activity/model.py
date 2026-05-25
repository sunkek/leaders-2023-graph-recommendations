from datetime import datetime
from enum import Enum
from random import choice

from pydantic.fields import Field
from pydantic.main import BaseModel
from pydantic.networks import EmailStr

from app.core.common import ObjectIdStr


class ActivityType(str, Enum):
    view = "view"
    favorite = "favorite"
    order = "order"  # TODO не реализован


class OfferType(str, Enum):
    event = "event"  # view, favorite
    excursion = "excursion"  # view, favorite
    hotel = "hotel"  # view
    place = "place"  #
    restaurant = "restaurant"  # view, favorite
    route = "route"  # view, favorite
    tour = "tour"  # view, favorite
    track = "track"  # view, favorite


class Activity(BaseModel):
    # user_id: UUID
    user_email: EmailStr  # TODO Используется для удобства демонстрации, заменить на user id
    offer_id: ObjectIdStr
    offer_type: OfferType
    type: ActivityType
    count: int | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)
