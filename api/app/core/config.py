from pydantic import BaseSettings

from app.core.common import Environment


class Config(BaseSettings):
    ENVIRONMENT: Environment = Environment.development
    NEEDS_IMPORT: bool = False
    LOG_LEVEL: str = "info"

    API_HOST: str = "localhost"
    API_PORT: int = 80

    NEO4J_HOST: str = "localhost"
    NEO4J_PORT: int = 7687
    NEO4J_USER: str = "neo4j"
    NEO4J_PASS: str = "neo4j"
    NEO4J_DB: str = "neo4j"

    CORS_ORIGINS: list[str] = ["*"]
    CORS_METHODS: list[str] = ["*"]
    CORS_HEADERS: list[str] = ["*"]

    def get_neo4j_uri(self) -> str:
        return f"neo4j://{self.NEO4J_HOST}:{self.NEO4J_PORT}"

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = True
