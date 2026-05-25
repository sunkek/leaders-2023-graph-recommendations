from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from app.core.common import ObjectIdStr


class Id(BaseModel):
    oid: str = Field(..., alias='$oid')


class SelectedItem(BaseModel):
    id: ObjectIdStr
    active: bool


class RouteData(BaseModel):
    dictionaries: list[ObjectIdStr]
    selected: list[SelectedItem]
    active: list[ObjectIdStr]


class DictionaryData(BaseModel):
    region: str
    city: str
    time: str
    packet_price: int
    route_tags: list
    route: RouteData
    import_denied: bool


class RouteNested(BaseModel):
    id: Id = Field(..., alias='_id')
    dictionary_data: DictionaryData

    def get_flat_model(self) -> Route:
        obj = Route(
            id=self.id.oid,
            region_id=self.dictionary_data.region,
            city_id=self.dictionary_data.city,
            duration=self.dictionary_data.time,
            price=self.dictionary_data.packet_price,
            tags=self.dictionary_data.route_tags,
            route=self.dictionary_data.route,
            import_denied=self.dictionary_data.import_denied,
        )
        if route := self.dictionary_data.route:
            obj.items = route.active
        return obj

class Route(BaseModel):
    id: ObjectIdStr
    region_id: ObjectIdStr
    city_id: ObjectIdStr
    duration: str
    price: int
    tags: list[ObjectIdStr]
    items: list[ObjectIdStr] | None = Field(default=None)
    import_denied: bool
    updated_at: datetime | None = Field(default=None)
