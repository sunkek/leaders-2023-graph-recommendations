from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from app.core.common import ObjectIdStr


class Id(BaseModel):
    oid: str = Field(..., alias='$oid')


class SessionId(BaseModel):
    id: str
    startTime: datetime
    endTime: datetime | None = Field(default=None)
    timezone: str
    isAllDay: bool


class Start(BaseModel):
    date: str = Field(..., alias='$date')


class End(BaseModel):
    date: str = Field(..., alias='$date')


class ScheduleItem(BaseModel):
    title: str
    start: Start
    end: End


class TimetableByPlaceItem(BaseModel):
    placeId: str
    sessionIds: list[SessionId]
    schedule: list[ScheduleItem]


class DictionaryData(BaseModel):
    region: str | None = Field(default=None)
    city: str | None = Field(default=None)
    event_type: str | None = Field(default=None)
    duration: str | None = Field(default=None)
    ticket_price: str | None = Field(default=None)
    age: str | None = Field(default=None)
    place: list[str]
    restaurants: list[str]
    tags: list[str]
    import_denied: bool | None = Field(default=None)


class EventNested(BaseModel):
    id: Id = Field(..., alias='_id')
    dictionary_data: DictionaryData

    def get_flat_model(self) -> Event:
        return Event(
            id=self.id.oid,
            region_id=self.dictionary_data.region,
            city_id=self.dictionary_data.city,
            event_type_id=self.dictionary_data.event_type,
            place_ids=self.dictionary_data.place,
            restaurant_ids=self.dictionary_data.restaurants,
            tags=self.dictionary_data.tags,
            duration=self.dictionary_data.duration,
            ticket_price=self.dictionary_data.ticket_price,
            age_restriction=self.dictionary_data.age,
            import_denied=self.dictionary_data.import_denied,
        )

class Event(BaseModel):
    id: ObjectIdStr
    region_id: ObjectIdStr | None = Field(default=None)
    city_id: ObjectIdStr | None = Field(default=None)
    event_type_id: ObjectIdStr | None = Field(default=None)
    place_ids: list[ObjectIdStr]
    restaurant_ids: list[ObjectIdStr]
    tags: list[ObjectIdStr]
    duration: int | None = Field(default=None)
    ticket_price: int | None = Field(default=None)
    age_restriction: str | None = Field(default=None)
    import_denied: bool | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)
