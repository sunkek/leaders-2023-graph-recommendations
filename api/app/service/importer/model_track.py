from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from app.core.common import ObjectIdStr


class Id(BaseModel):
    oid: str = Field(..., alias='$oid')

class SelectedItem(BaseModel):
    id: ObjectIdStr
    active: bool

class DayContents(BaseModel):
    dictionaries: list[ObjectIdStr]
    selected: list[SelectedItem]
    active: list[ObjectIdStr]

class RouteItem(BaseModel):
    day_contents: DayContents

class DictionaryData(BaseModel):
    region: str
    city: str
    route: list[RouteItem]
    tags: list[str]
    price: int
    duration_hours: int
    days_count: int | None = Field(default=None)
    type: str
    import_denied: bool


class TrackNested(BaseModel):
    id: Id = Field(..., alias='_id')
    dictionary_data: DictionaryData

    def get_flat_model(self) -> Track:
        obj = Track(
            id=self.id.oid,
            region_id=self.dictionary_data.region,
            city_id=self.dictionary_data.city,
            route=self.dictionary_data.route,
            tags=self.dictionary_data.tags,
            price=self.dictionary_data.price,
            duration_hours=self.dictionary_data.duration_hours,
            days_count=self.dictionary_data.days_count,
            type=self.dictionary_data.type,
            import_denied=self.dictionary_data.import_denied,
        )
        obj.items = []
        for day in self.dictionary_data.route:
            obj.items.extend(day.day_contents.active)
        return obj

class Track(BaseModel):
    id: ObjectIdStr
    region_id: str
    city_id: str
    items: list[ObjectIdStr] | None = Field(default=None)
    tags: list[ObjectIdStr]
    price: int
    duration_hours: int
    days_count: int | None = Field(default=None)
    type: ObjectIdStr
    import_denied: bool
    updated_at: datetime | None = Field(default=None)
