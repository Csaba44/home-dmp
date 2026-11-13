import json
from typing import Any

import paho.mqtt.client as mqtt
from paho.mqtt.client import ConnectFlags, MQTTMessage
from paho.mqtt.properties import Properties
from paho.mqtt.reasoncodes import ReasonCode

from mqtt.client import mqttc
from notifications import NOTIFICATIONS

from loguru import logger


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
    logger.info(f"topic={msg.topic} retain={msg.retain} payload={msg.payload!r}")
    if msg.topic in NOTIFICATIONS:
        NOTIFICATIONS[msg.topic](json.loads(msg.payload.decode()))


def main() -> None:
    logger.add("logs/app.log", rotation="10 MB", retention="14 days")
    print("Notification services - started")

    mqttc.on_connect = on_connect
    mqttc.on_message = on_message

    try:
        mqttc.loop_forever()
    except KeyboardInterrupt:
        print("Shutting down")
        mqttc.disconnect()


if __name__ == "__main__":
    main()
