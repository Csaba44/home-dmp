import requests
from loguru import logger

from config import cfg


def notify(msg: str) -> None:
    try:
        response = requests.post(
            f"https://ntfy.sh/{cfg.ntfy_topic_prefix}-{cfg.ntfy_topic}",
            data=msg.encode("utf-8"),
            timeout=10,
        )
        response.raise_for_status()
        logger.info("Notification sent")
    except requests.RequestException:
        logger.exception("Failed to send notification: {!r}", msg)
