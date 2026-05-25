from fastapi import APIRouter

from app.resource.activity.model import Activity
from app.resource.activity.schema import CreateActivityRequest
from app.service.database import db

router = APIRouter(
    prefix="/activity",
    tags=["activity"],
)


@router.post("", response_model=bool)
async def post_activity(activity: CreateActivityRequest):
    """Создаёт запись об активности пользователя"""
    # TODO Использовать access token пользователя для аутентификации
    data = db.upsert_activity(Activity(**activity.dict()))
    return bool(data)

# TODO Добавить эндпоинт для удаления из избранного
