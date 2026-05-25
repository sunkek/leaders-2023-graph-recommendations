from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from app.core.common import ObjectIdStr


class Id(BaseModel):
    oid: str = Field(..., alias='$oid')


class SeasonEnd(BaseModel):
    date: str = Field(..., alias='$date')


class SeasonStart(BaseModel):
    date: str = Field(..., alias='$date')


class SelectedItem(BaseModel):
    id: ObjectIdStr
    active: bool


class DayContents(BaseModel):
    dictionaries: list[ObjectIdStr]
    selected: list[SelectedItem] | None = Field(default=None)
    active: list[ObjectIdStr] | None = Field(default=None)


class RouteItem(BaseModel):
    events: list
    day_contents: DayContents | None = Field(default=None)


class DictionaryData(BaseModel):
    region: str
    city: str | None = Field(default=None)
    tags: list[str]
    season_start: SeasonStart | datetime | None = Field(default=None)
    season_end: SeasonEnd | datetime | None = Field(default=None)
    price: str
    hotel_stars: str | None = Field(default=None)
    min_age: str | None = Field(default=None)
    complexity: str | None = Field(default=None)
    days: int
    nights: int
    route: list[RouteItem]
    tour_type: str | None = Field(default=None)
    import_denied: bool | None = Field(default=None)


class TourNested(BaseModel):
    id: Id = Field(..., alias='_id')
    dictionary_data: DictionaryData

    def get_flat_model(self) -> Tour:
        obj = Tour(
            id=self.id.oid,
            region_id=self.dictionary_data.region,
            city_id=self.dictionary_data.city,
            tags=self.dictionary_data.tags,
            price=self.dictionary_data.price.replace(" ", ""),
            hotel_stars=self.dictionary_data.hotel_stars,
            min_age=self.dictionary_data.min_age,
            complexity=self.dictionary_data.complexity,
            days=self.dictionary_data.days,
            nights=self.dictionary_data.nights,
            route=self.dictionary_data.route,
            tour_type=self.dictionary_data.tour_type,
            import_denied=self.dictionary_data.import_denied,
        )
        if self.dictionary_data.season_start:
            if isinstance(self.dictionary_data.season_start, SeasonStart):
                obj.season_start = self.dictionary_data.season_start.date
            else:
                obj.season_start = self.dictionary_data.season_start
        if self.dictionary_data.season_end:
            if isinstance(self.dictionary_data.season_end, SeasonEnd):
                obj.season_end = self.dictionary_data.season_end.date
            else:
                obj.season_end = self.dictionary_data.season_end
        obj.items = []
        for day in self.dictionary_data.route:
            if day_contents := day.day_contents:
                if active := day_contents.active:
                    obj.items.extend(active)
        return obj

class Tour(BaseModel):
    id: ObjectIdStr
    region_id: ObjectIdStr
    city_id: ObjectIdStr | None = Field(default=None)
    tags: list[ObjectIdStr]
    season_start: datetime | None = Field(default=None)
    season_end: datetime | None = Field(default=None)
    price: int
    hotel_stars: str | None = Field(default=None)
    min_age: str | None = Field(default=None)
    complexity: str | None = Field(default=None)
    days: int
    nights: int
    tour_type: str | None = Field(default=None)
    items: list[ObjectIdStr] | None = Field(default=None)
    import_denied: bool | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)
