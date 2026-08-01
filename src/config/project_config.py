from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()


class _GigaChatSettings(BaseSettings):
    """ настройки GigaChatAPI"""
    model_config = SettingsConfigDict(env_prefix="GIGA_CHAT_")
    auth_key: str
    model: str = "GigaChat-2-Max"
    scope: str = "GIGACHAT_API_PERS"
    temperature: float = 0.3
    max_tokens: int = 1024


class _AppSettings(BaseSettings):
    """ глобальные настройки проекта"""
    port: int = 8000


class Settings(BaseSettings):
    """ все настройки в одном месте """
    app: _AppSettings = _AppSettings()
    gigachat: _GigaChatSettings = _GigaChatSettings()


settings = Settings()
