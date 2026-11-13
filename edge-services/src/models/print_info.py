import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime

import paho.mqtt.client as mqtt

MATCH_TOPICS = ["octoPrint/progress/printing"]
PUBLISH_TOPIC = "home/dmp/3d/print_info"


@dataclass
class PrintProgress:
    print_name: str
    progress: float
    timestamp: datetime

    def publish(self, client: mqtt.Client) -> None:
        data = asdict(self)
        data["timestamp"] = self.timestamp.isoformat()
        client.publish(PUBLISH_TOPIC, json.dumps(data), qos=1)


def parse_print_info(payload: dict) -> PrintProgress:
    name = payload["path"].split("/")[-1]  # "Bottom_Hex_SM_PLA_15m5s.gcode"
    name = name.removesuffix(".gcode")  # "Bottom_Hex_SM_PLA_15m5s"
    name = name.rsplit("_", 1)[0]

    return PrintProgress(
        print_name=name,
        progress=float(payload["progress"]),
        timestamp=datetime.fromtimestamp(payload["_timestamp"], tz=UTC),
    )
