from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from app.core.common import ObjectIdStr


class Id(BaseModel):
    oid: str = Field(..., alias='$oid')


class DictionaryData(BaseModel):
    price_hotel: int | None = Field(default=None)
    country: str
    import_denied: bool | None = Field(default=None)
    title: str


class RegionNested(BaseModel):
    id: Id = Field(..., alias='_id')
    dictionary_data: DictionaryData

    def get_flat_model(self) -> Region:
        return Region(
            id=self.id.oid,
            country_id=self.dictionary_data.country,
            price_hotel=self.dictionary_data.price_hotel,
            import_denied=self.dictionary_data.import_denied,
        )

class Region(BaseModel):
    id: ObjectIdStr
    country_id: ObjectIdStr
    price_hotel: int | None = Field(default=None)
    import_denied: bool | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)
