from pydantic.main import BaseModel
from pydantic.networks import EmailStr

from app.core.common import ObjectIdStr
from app.resource.activity.model import ActivityType, OfferType


class CreateActivityRequest(BaseModel):
    user_email: EmailStr  # TODO Используется для удобства демонстрации, заменить на user id
    offer_id: ObjectIdStr
    offer_type: OfferType
    type: ActivityType
