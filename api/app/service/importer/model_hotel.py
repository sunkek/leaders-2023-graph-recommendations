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
    geo_data: GeoData | None = Field(default=None)
    region: str
    city: str | None = Field(default=None)
    stars: str | None = Field(default=None)
    facility_services: list[str]
    beach_services: list[str]
    entertainment_services: list[str]
    fitness_services: list[str]
    common_services: list[str]
    meals: list[str]
    import_denied: bool | None = Field(default=None)


class HotelNested(BaseModel):
    id: Id = Field(..., alias='_id')
    dictionary_data: DictionaryData

    def get_flat_model(self) -> Hotel:
        hotel = Hotel(
            id=self.id.oid,
            region_id=self.dictionary_data.region,
            city_id=self.dictionary_data.city,
            stars=self.dictionary_data.stars,
            facility_services=self.dictionary_data.facility_services,
            beach_services=self.dictionary_data.beach_services,
            entertainment_services=self.dictionary_data.entertainment_services,
            fitness_services=self.dictionary_data.fitness_services,
            common_services=self.dictionary_data.common_services,
            meals=self.dictionary_data.meals,
            import_denied=self.dictionary_data.import_denied,
        )
        if self.dictionary_data.geo_data.coordinates:
            hotel.lat = self.dictionary_data.geo_data.coordinates[0]
            hotel.lng = self.dictionary_data.geo_data.coordinates[1]
        if self.dictionary_data.geo_data.center_distance:
            hotel.center_distance = self.dictionary_data.geo_data.center_distance
        return hotel

class Hotel(BaseModel):
    id: ObjectIdStr
    region_id: ObjectIdStr
    city_id: ObjectIdStr | None = Field(default=None)
    stars: int | None = Field(default=None)
    lat: float | None = Field(default=None)
    lng: float | None = Field(default=None)
    center_distance: float | None = Field(default=None)
    facility_services: list[ObjectIdStr]
    beach_services: list[ObjectIdStr]
    entertainment_services: list[ObjectIdStr]
    fitness_services: list[ObjectIdStr]
    common_services: list[ObjectIdStr]
    meals: list[ObjectIdStr]
    import_denied: bool | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)
