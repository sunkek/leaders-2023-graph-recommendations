from datetime import datetime
from enum import Enum

from pydantic.fields import Field
from pydantic.main import BaseModel
from pydantic.networks import EmailStr

from app.core.common import ObjectIdStr


class Sex(str, Enum):
    male = "male"
    female = "female"


class FamilyStatus(str, Enum):
    married = "married"
    in_relationship = "in_relationship"
    single = "single"


class TourismGoal(str, Enum):
    active = "active"
    calm = "calm"
    cultural = "cultural"
    social = "social"


class Questionnaire(BaseModel):
    # user_id: UUID = Field(default_factory=uuid4)
    email: EmailStr  # TODO Используется для удобства демонстрации, заменить на user id
    birthday_at: datetime | None = Field(default=None)
    sex: Sex | None = Field(default=None)
    family_status: FamilyStatus | None = Field(default=None)
    has_children_below_18: bool | None = Field(default=None)
    tourism_goals: list[TourismGoal] | None = Field(default=None)
    region: ObjectIdStr | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)
