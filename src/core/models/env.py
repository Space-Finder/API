__all__ = ("Settings",)

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PORT: int = 8443
    DATABASE_URL: str
    DEVMODE: bool
    BASE_URL: str
    ACCESS_TOKEN_SECRET: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
