from typing import Any

import paho.mqtt.client as mqtt
from models import PARSERS
from mqtt.client import mqttc
from normalizer.normalize import normalize
from paho.mqtt.client import ConnectFlags, MQTTMessage
from paho.mqtt.properties import Properties
from paho.mqtt.reasoncodes import ReasonCode


def on_connect(
    client: mqtt.Client,
    userdata: Any,
    flags: ConnectFlags,
    reason_code: ReasonCode,
    properties: Properties | None,
) -> None:
    print(f"Connected with result code: {reason_code}")
    for topic in PARSERS:
        client.subscribe(topic, 1)


def on_message(client: mqtt.Client, userdata: Any, msg: MQTTMessage) -> None:
    if "octoPrint/" in msg.topic:
        normalize(msg.topic, msg.payload.decode())


def main() -> None:
    print("Hello Edge")

    mqttc.on_connect = on_connect
    mqttc.on_message = on_message

    try:
        mqttc.loop_forever()
    except KeyboardInterrupt:
        print("Shutting down")
        mqttc.disconnect()


if __name__ == "__main__":
    main()
