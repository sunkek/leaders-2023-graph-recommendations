import uvicorn
from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware

from app.core import config
from app.service.rest.router import activity
from app.service.rest.router import questionnaire
from app.service.rest.router import recommendation


class Api(FastAPI):
    def __init__(self, **extra: any):
        super().__init__(**extra)

    def run(self, host: str, port: int, log_level: str = "info"):
        uvicorn.run(self, host=host, port=port, log_level=log_level)


api = Api(debug=not config.ENVIRONMENT.is_production())

api.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=config.CORS_METHODS,
    allow_headers=config.CORS_HEADERS,
)


@api.get("/health", include_in_schema=False)
async def health() -> Response:
    return Response(status_code=200)


api.include_router(activity)
api.include_router(questionnaire)
api.include_router(recommendation)
