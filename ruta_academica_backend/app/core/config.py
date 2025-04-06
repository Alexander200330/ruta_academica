from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_PREFIX: str = "/api/v1"
    API_TITLE: str = "RutaAcadémica API"
    API_DESCRIPTION: str = (
        "API para análisis de prerrequisitos académicos mediante grafos dirigidos"
    )
    API_VERSION: str = "0.1.0"

    DATABASE_URL: str = "sqlite:///./ruta_academica.db"

    class Config:
        env_file = ".env"


settings = Settings()
