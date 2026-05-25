from __future__ import annotations

from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from app.core.common import ObjectIdStr


class Id(BaseModel):
    oid: str = Field(..., alias='$oid')


class GeoData(BaseModel):
    coordinates: List[float]


class DictionaryData(BaseModel):
    country: list[str]
    region: str | None = Field(default=None)
    geo_data: GeoData | None = Field(default=None)
    import_denied: bool | None = Field(default=None)


class CityNested(BaseModel):
    id: Id = Field(..., alias='_id')
    dictionary_data: DictionaryData

    def get_flat_model(self) -> City:
        obj = City(
            id=self.id.oid,
            country_ids=self.dictionary_data.country,
            region_id=self.dictionary_data.region,
            import_denied=self.dictionary_data.import_denied,
        )
        if self.dictionary_data.geo_data.coordinates:
            obj.lat=self.dictionary_data.geo_data.coordinates[0]
            obj.lng=self.dictionary_data.geo_data.coordinates[1]
        return obj


class City(BaseModel):
    id: ObjectIdStr
    country_ids: list[ObjectIdStr]
    region_id: ObjectIdStr | None = Field(default=None)
    lat: float | None = Field(default=None)
    lng: float | None = Field(default=None)
    import_denied: bool | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)
