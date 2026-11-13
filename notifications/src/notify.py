import requests
from loguru import logger

from config import settings


def notify(msg: str) -> None:
    try:
        response = requests.post(
            f"https://ntfy.sh/{settings.ntfy_topic}",
            data=msg.encode("utf-8"),
            timeout=10,
        )
        response.raise_for_status()
    except requests.RequestException:
        logger.exception("Failed to send notification: {!r}", msg)
