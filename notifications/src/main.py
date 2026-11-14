import json
from pathlib import Path
from typing import Any

import paho.mqtt.client as mqtt
from loguru import logger
from paho.mqtt.client import ConnectFlags, MQTTMessage
from paho.mqtt.properties import Properties
from paho.mqtt.reasoncodes import ReasonCode

from config import cfg
from mqtt.client import mqttc
from notifications import NOTIFICATIONS


def on_connect(
    client: mqtt.Client,
    userdata: Any,
    flags: ConnectFlags,
    reason_code: ReasonCode,
    properties: Properties | None,
) -> None:
    for topic in NOTIFICATIONS:
        client.subscribe(topic, 1)


def on_message(client: mqtt.Client, userdata: Any, msg: MQTTMessage) -> None:
    if msg.retain:
        logger.info(f"Skipping retained message: payload={msg.payload!r}")
        return
    logger.info(f"topic={msg.topic} retain={msg.retain} payload={msg.payload!r}")
    if msg.topic in NOTIFICATIONS:
        NOTIFICATIONS[msg.topic](json.loads(msg.payload.decode()))


def main() -> None:
    logger.add(
        Path("~/.homefloor/log-notifications.txt").expanduser(),
        rotation="10 MB",
        retention="14 days",
    )
    print("Notification services - started")
    print(f"ntfy.sh topic: {cfg.ntfy_topic_prefix}-{cfg.ntfy_topic}")

    mqttc.on_connect = on_connect
    mqttc.on_message = on_message

    try:
        mqttc.loop_forever()
    except KeyboardInterrupt:
        print("Shutting down")
        mqttc.disconnect()


if __name__ == "__main__":
    main()
