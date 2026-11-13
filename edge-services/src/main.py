from config import settings

import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion


def on_connect(client, userdata, flags, reason_code, properties) -> None:
    print(f"Connected with result code {reason_code}")
    client.subscribe("octoPrint/#", 1)

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    


def main() -> None:
  print("Hello Edge")
  
  mqttc = mqtt.Client(CallbackAPIVersion.VERSION2)
  mqttc.on_connect = on_connect
  mqttc.on_message = on_message

  mqttc.username_pw_set(settings.mqtt_user, settings.mqtt_password.get_secret_value())
  mqttc.connect(settings.mqtt_host, settings.mqtt_port, 60)
  
  try:
      mqttc.loop_forever()
  except KeyboardInterrupt:
      print("Shutting down")
      mqttc.disconnect()

if __name__ == "__main__":
  main()