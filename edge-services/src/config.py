from pathlib import Path

from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

CONFIG_FILE = Path("/var/lib/homefloor/config.json")


class AppConfig(BaseModel):
    mqtt_topic: str = "homefloor/3d"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    mqtt_host: str
    mqtt_port: int = 1883
    mqtt_user: str
    mqtt_password: SecretStr


def save(cfg: AppConfig) -> None:
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(cfg.model_dump_json(indent=2))


def load() -> AppConfig:
    if CONFIG_FILE.exists():
        return AppConfig.model_validate_json(CONFIG_FILE.read_text())
    return AppConfig()


settings = Settings()

cfg = load()
