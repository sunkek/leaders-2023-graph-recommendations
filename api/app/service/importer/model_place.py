from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field
from pydantic.class_validators import validator

from app.core.common import ObjectIdStr


class Id(BaseModel):
    oid: str = Field(..., alias='$oid')


class GeoData(BaseModel):
    coordinates: list[float] | None = Field(default=None)
    type: str | None = Field(default=None)
    center_distance: float | None = Field(default=None)


class DictionaryData(BaseModel):
    country: list[str] | None = Field(default=None)
    region: str | None = Field(default=None)
    city: list[str | None] | None = Field(default=None)
    geo_data: GeoData | None = Field(default=None)
    tags: list[str] | None = Field(default=None)
    import_denied: bool | None = Field(default=None)

    @validator("city")
    def remove_none_from_list(cls, v):
        if v is None:
            return None
        return [i for i in v if i is not None]


class PlaceNested(BaseModel):
    id: Id = Field(..., alias='_id')
    dictionary_data: DictionaryData

    def get_flat_model(self) -> Place:
        place = Place(
            id=self.id.oid,
            country_ids=self.dictionary_data.country,
            region_id=self.dictionary_data.region,
            city_ids=self.dictionary_data.city,
            tags=self.dictionary_data.tags,
            import_denied=self.dictionary_data.import_denied,
        )
        if self.dictionary_data.geo_data:
            if self.dictionary_data.geo_data.coordinates:
                place.lat = self.dictionary_data.geo_data.coordinates[0]
                place.lng = self.dictionary_data.geo_data.coordinates[1]
            if self.dictionary_data.geo_data.center_distance:
                place.center_distance = self.dictionary_data.geo_data.center_distance
        return place

class Place(BaseModel):
    id: ObjectIdStr
    country_ids: list[ObjectIdStr] | None = Field(default=None)
    region_id: ObjectIdStr | None = Field(default=None)
    city_ids: list[ObjectIdStr] | None = Field(default=None)
    tags: list[ObjectIdStr] | None = Field(default=None)
    lat: float | None = Field(default=None)
    lng: float | None = Field(default=None)
    center_distance: float | None = Field(default=None)
    import_denied: bool | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)
