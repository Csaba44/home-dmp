from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    mqtt_host: str
    mqtt_port: int = 1883
    mqtt_user: str
    mqtt_password: SecretStr


settings = Settings()
