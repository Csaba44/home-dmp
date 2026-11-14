import json

from loguru import logger

from models import PARSERS
from mqtt.client import mqttc


def normalize(topic: str, payload: str) -> None:
    try:
        parsed_payload = json.loads(payload)
    except json.JSONDecodeError:
        logger.warning(f"Non json payload skipped (while normalizing), topic: {topic}")
        return

    model = PARSERS[topic](parsed_payload)
    model.publish(mqttc)
