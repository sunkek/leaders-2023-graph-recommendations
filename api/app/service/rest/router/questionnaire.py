from fastapi import APIRouter
from pydantic.networks import EmailStr

from app.resource.questionnaire.model import Questionnaire
from app.resource.questionnaire.schema import GetQuestionnaireResponse, UpdateQuestionnaireResponse, \
    UpdateQuestionnaireRequest
from app.service.database import db

router = APIRouter(
    prefix="/questionnaire",
    tags=["questionnaire"],
)


@router.get("", response_model=GetQuestionnaireResponse)
async def get_questionnaire_data(email: EmailStr):
    """Возвращает анкетные данные текущего пользователя"""
    # TODO Использовать access token пользователя для аутентификации
    data = db.get_questionnaire(email)
    return GetQuestionnaireResponse(**data)


@router.post("", response_model=UpdateQuestionnaireResponse)
async def post_questionnaire_data(email: EmailStr, questionnaire: UpdateQuestionnaireRequest):
    """Перезаписывает анкетные данные пользователя"""
    # TODO Использовать access token пользователя для аутентификации
    data = db.upsert_questionnaire(Questionnaire(email=email, **questionnaire.dict()))
    return UpdateQuestionnaireResponse(**data)
