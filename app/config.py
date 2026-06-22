from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        env_ignore_empty=True,
        extra='ignore',
    )

    database_url: str

    # zapi_instance: str
    # zapi_base_url: str
    # zapi_token: str
    # zapi_client_token: str | None = None

    wireweb_base_url: str
    wireweb_api_key: str
    wireweb_session_id: str

    # zapi_webhook_token: str
    wireweb_webhook_token: str
    providers_order: list[str] = ['wireweb']
    # providers_order: list[str] = ['zapi', 'wireweb']


settings = Settings()  # type: ignore
