from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class GigaChatSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="GIGA_CHAT_")
    auth_key: str
    model: str = "GigaChat-2-Max"
    scope: str = "GIGACHAT_API_PERS"
    temperature: float = 0.3
    max_tokens: int = 1024


class AppSettings(BaseSettings):
    port: int = 8000


class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    gigachat: GigaChatSettings = GigaChatSettings()


settings = Settings()
