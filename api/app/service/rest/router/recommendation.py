from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic.networks import EmailStr

from app.core.common import ObjectIdStr
from app.resource.activity.model import OfferType
from app.service.database import db

router = APIRouter(
    prefix="/recommendation",
    tags=["recommendation"],
)


async def recommendation_filters(
    region: ObjectIdStr | None = None,
    budget: int | None = None,
    date_start: datetime | None = None,
    date_end: datetime | None = None,
) -> dict[str, any]:
    return {
        "region": region,
        "date_start": date_start,
        "date_end": date_end,
        "budget": budget,
    }


@router.get("/user_based", response_model=list[ObjectIdStr])
async def get_user_based_recommendations(
    email: EmailStr,
    object_type: OfferType | None = OfferType.event,
    limit: int = 10,
    filters: Annotated[dict, Depends(recommendation_filters)] = None,
):
    """Возвращает объекты, которые привлекли внимание похожих по характеристикам пользователей"""
    # TODO Использовать access token пользователя для аутентификации
    data = db.get_user_based_recommendations(email, object_type, limit)
    return [ObjectIdStr(i["result"]["id"]) for i in data]


@router.get("/item_based", response_model=list[ObjectIdStr])
async def get_item_based_recommendations(
    email: EmailStr,
    object_id: ObjectIdStr,
    object_type: OfferType,
    limit: int = 10,
    filters: Annotated[dict, Depends(recommendation_filters)] = None,
):
    """Возвращает объекты, которые привлекли внимание похожих по поведению пользователей"""
    # TODO Использовать access token пользователя для аутентификации
    data = db.get_item_based_recommendations(email, object_id, object_type, limit)
    return [ObjectIdStr(i["result"]["id"]) for i in data]


@router.get("/similar", response_model=list[ObjectIdStr])
async def get_similar_recommendations(
    email: EmailStr,
    object_id: ObjectIdStr,
    object_type: OfferType,
    limit: int = 10,
    filters: Annotated[dict, Depends(recommendation_filters)] = None,
):
    """Возвращает объекты, похожие по свойствам"""
    # TODO Использовать access token пользователя для аутентификации
    data = db.get_similar_recommendations(email, object_id, object_type, limit)
    return [ObjectIdStr(i["result"]["id"]) for i in data]


@router.get("/popular", response_model=list[ObjectIdStr])
async def get_popular_recommendations(
    email: EmailStr,
    object_type: OfferType | None = OfferType.event,
    limit: int = 10,
    filters: Annotated[dict, Depends(recommendation_filters)] = None,
):
    """Возвращает объекты, на которые обращало внимание больше всего пользователей"""
    # TODO Использовать access token пользователя для аутентификации
    data = db.get_popular_recommendations(email, object_type, limit)
    return [ObjectIdStr(i["result"]["id"]) for i in data]
