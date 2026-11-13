from datetime import datetime

from loguru import logger

from notify import notify


def on_progress_change(payload: dict) -> None:
    try:
        if payload["progress"] != 100:
            return

        time = "?"
        try:
            time = datetime.fromisoformat(payload["timestamp"]).strftime("%H:%M")
        except (ValueError, TypeError, KeyError):
            logger.warning("Bad timestamp: {!r}", payload.get("timestamp"))

        notify(f"{payload['print_name']} finished printing at {time}")
        logger.info("Notified: {} finished at {}", payload["print_name"], time)

    except KeyError as e:
        logger.error("Payload missing key {}: {!r}", e, payload)
