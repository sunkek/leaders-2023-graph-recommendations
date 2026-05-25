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
    selected: list[SelectedItem] | None = Field(default=None)
    active: list[ObjectIdStr] | None = Field(default=None)


class RouteItem(BaseModel):
    day_contents: DayContents | None = Field(default=None)

class SeasonEnd(BaseModel):
    date: datetime = Field(alias='$date')


class SeasonStart(BaseModel):
    date: datetime = Field(alias='$date')


class DictionaryData(BaseModel):
    route: list[RouteItem]
    tags: list[str]
    duration_hours: float | None = Field(default=None)
    price: int
    city: str | None = Field(default=None)
    region: str
    language: list[str]
    min_age: str | None = Field(default=None)
    import_denied: bool | None = Field(default=None)


class ExcursionNested(BaseModel):
    id: Id = Field(..., alias='_id')
    dictionary_data: DictionaryData

    def get_flat_model(self) -> Excursion:
        obj = Excursion(
            id=self.id.oid,
            region_id=self.dictionary_data.region,
            city_id=self.dictionary_data.city,
            language_ids=self.dictionary_data.language,
            duration_hours=self.dictionary_data.duration_hours,
            price=self.dictionary_data.price,
            age_restriction=self.dictionary_data.min_age,
            import_denied=self.dictionary_data.import_denied,
            tags=self.dictionary_data.tags,
        )
        if route := self.dictionary_data.route:
            if day_contents := route[0].day_contents:
                obj.items = day_contents.active
        return obj

class Excursion(BaseModel):
    id: ObjectIdStr
    region_id: ObjectIdStr
    city_id: ObjectIdStr | None = Field(default=None)
    language_ids: list[ObjectIdStr]
    tags: list[ObjectIdStr]
    items: list[ObjectIdStr] | None = Field(default=None)
    duration_hours: float | None = Field(default=None)
    price: int
    age_restriction: str | None = Field(default=None)
    import_denied: bool | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)
