from pydantic.main import BaseModel

from app.core.common import ObjectIdStr


class Recommendation(BaseModel):
    offers: list[ObjectIdStr]
