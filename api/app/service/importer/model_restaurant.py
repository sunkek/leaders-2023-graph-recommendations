from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from app.core.common import ObjectIdStr


class Id(BaseModel):
    oid: str = Field(..., alias='$oid')


class GeoData(BaseModel):
    coordinates: list[float]
    center_distance: float | None = Field(default=None)


class DictionaryData(BaseModel):
    country: list[str] | None = Field(default=None)
    region: str | None = Field(default=None)
    city: list[str]
    avg_time_visit: int | None = Field(default=None)
    bill: int | None = Field(default=None)
    tags: list[str] | None = Field(default=None)
    cuisines: list[str] | None = Field(default=None)
    geo_data: GeoData | None = Field(default=None)
    import_denied: bool | None = Field(default=None)

class RestaurantNested(BaseModel):
    id: Id = Field(..., alias='_id')
    dictionary_data: DictionaryData

    def get_flat_model(self) -> Restaurant:
        obj = Restaurant(
            id=self.id.oid,
            country_ids=self.dictionary_data.country,
            region_id=self.dictionary_data.region,
            city_ids=self.dictionary_data.city,
            avg_check=self.dictionary_data.bill,
            avg_visit_time=self.dictionary_data.avg_time_visit,
            tags=self.dictionary_data.tags,
            cuisines=self.dictionary_data.cuisines,
            import_denied=self.dictionary_data.import_denied,
        )
        if self.dictionary_data.geo_data:
            if self.dictionary_data.geo_data.coordinates:
                obj.lat = self.dictionary_data.geo_data.coordinates[0]
                obj.lng = self.dictionary_data.geo_data.coordinates[1]
            if self.dictionary_data.geo_data.center_distance:
                obj.center_distance = self.dictionary_data.geo_data.center_distance
        return obj

class Restaurant(BaseModel):
    id: ObjectIdStr
    country_ids: list[ObjectIdStr] | None = Field(default=None)
    region_id: ObjectIdStr | None = Field(default=None)
    city_ids: list[ObjectIdStr]
    avg_check: int | None = Field(default=None)
    avg_visit_time: int | None = Field(default=None)
    tags: list[ObjectIdStr] | None = Field(default=None)
    cuisines: list[ObjectIdStr] | None = Field(default=None)
    lat: float | None = Field(default=None)
    lng: float | None = Field(default=None)
    center_distance: float | None = Field(default=None)
    import_denied: bool | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)
