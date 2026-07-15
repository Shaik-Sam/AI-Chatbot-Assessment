from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    max_history_messages: int = 20
    max_tokens: int = 1024
    temperature: float = 0.7
    host: str = "0.0.0.0"
    port: int = 8000


settings = Settings()
