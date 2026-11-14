import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime

import paho.mqtt.client as mqtt
from loguru import logger

from config import cfg

MATCH_TOPICS = ["octoPrint/progress/printing"]
PUBLISH_TOPIC = f"{cfg.mqtt_topic}/print_info"


@dataclass
class PrintProgress:
    print_name: str
    progress: int
    timestamp: datetime

    def publish(self, client: mqtt.Client) -> None:
        data = asdict(self)
        data["timestamp"] = self.timestamp.isoformat()
        client.publish(PUBLISH_TOPIC, json.dumps(data), qos=1)


def parse_print_info(payload: dict) -> PrintProgress:
    name = "unknown"
    try:
        name = payload["path"].split("/")[-1]  # "Bottom_Hex_SM_PLA_15m5s.gcode"
        name = name.removesuffix(".gcode")  # "Bottom_Hex_SM_PLA_15m5s"
        name = name.rsplit("_", 1)[0]
    except (KeyError, AttributeError):
        logger.warning(f"path not in correct format - payload = {payload}")

    return PrintProgress(
        print_name=name,
        progress=int(payload["progress"]),
        timestamp=datetime.fromtimestamp(payload["_timestamp"], tz=UTC),
    )
