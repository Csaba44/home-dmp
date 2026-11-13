import secrets
from pathlib import Path

from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

CONFIG_FILE = Path("/app/data/config.json")


class AppConfig(BaseModel):
    ntfy_topic: str | None = None
    notify_on_finish: bool = True


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
if cfg.ntfy_topic is None:
    cfg.ntfy_topic = f"home-dmp-{secrets.token_urlsafe(16)}"
    save(cfg)
