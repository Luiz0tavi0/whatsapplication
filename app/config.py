import os
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.getenv('TEST_ENV_FILE', '.env'),
        env_file_encoding='utf-8',
        env_ignore_empty=True,
        extra='ignore',
    )

    DATABASE_URL: str

    ZAPI_INSTANCE: str
    ZAPI_BASE_URL: str
    ZAPI_TOKEN: str
    ZAPI_WEBHOOK_TOKEN: str
    WIREWEB_BASE_URL: Optional[str] = None
    WIREWEB_API_KEY: Optional[str] = None
    WIREWEB_SESSION_ID: Optional[str] = None
    WIREWEB_WEBHOOK_TOKEN: Optional[str] = None
    PROVIDERS_ORDER: tuple[str, ...] = ('zapi', 'wireweb')


settings = Settings()  # type: ignore
