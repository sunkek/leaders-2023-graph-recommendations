from datetime import datetime

from pydantic.class_validators import validator
from pydantic.fields import Field
from pydantic.main import BaseModel

from app.core.common import ObjectIdStr
from app.resource.questionnaire.regions import regions
from app.resource.questionnaire.model import FamilyStatus, Sex, TourismGoal

regions_joined = ', '.join(regions)


class GetQuestionnaireResponse(BaseModel):
    birthday_at: datetime | None = Field(default=None)
    sex: Sex | None = Field(default=None)
    family_status: FamilyStatus | None = Field(default=None)
    has_children_below_18: bool | None = Field(default=None)
    tourism_goals: list[TourismGoal] | None = Field(default=None)
    region: ObjectIdStr | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)


class UpdateQuestionnaireRequest(BaseModel):
    # id: UUID
    birthday_at: datetime | None = Field(default=None)
    sex: Sex | None = Field(default=None)
    family_status: FamilyStatus | None = Field(default=None)
    has_children_below_18: bool | None = Field(default=None)
    tourism_goals: list[TourismGoal] | None = Field(default=None)
    region: ObjectIdStr | None = Field(default=None)

    @validator("region")
    def in_regions(cls, v):
        if v in regions:
            return v
        raise ValueError(f"Invalid value for 'field'. Allowed values are: {regions_joined}")


class UpdateQuestionnaireResponse(BaseModel):
    birthday_at: datetime | None = Field(default=None)
    sex: Sex | None = Field(default=None)
    family_status: FamilyStatus | None = Field(default=None)
    has_children_below_18: bool | None = Field(default=None)
    tourism_goals: list[TourismGoal] | None = Field(default=None)
    region: ObjectIdStr | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)
