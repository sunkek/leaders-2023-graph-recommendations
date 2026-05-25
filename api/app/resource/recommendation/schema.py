from datetime import datetime

from pydantic import BaseModel, Field

from app.core.common import ObjectIdStr


class GetFilteredRecommendationRequest(BaseModel):
    region: ObjectIdStr | None = Field(default=None)
    date_start: datetime | None = Field(default=None)
    date_end: datetime | None = Field(default=None)
    price_from: int | None = Field(default=None)
    price_to: int | None = Field(default=None)
