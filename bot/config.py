import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    BOT_TOKEN: str = Field(default="", description="Telegram Bot Token from @BotFather")
    API_BASE_URL: str = Field(default="http://127.0.0.1:8000/api", description="Django REST API base URL")
    BACKEND_HOST: str = Field(default="http://127.0.0.1:8000", description="Backend host for media files")
    ADMIN_IDS: list[int] = Field(default=[], description="Telegram admin user IDs")
    ADMIN_GROUP_CHAT_ID: int = Field(default=0, description="Telegram Group Chat ID for orders notification")


    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
