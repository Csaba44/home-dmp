import paho.mqtt.client as mqtt
from config import settings
from paho.mqtt.enums import CallbackAPIVersion

mqttc = mqtt.Client(CallbackAPIVersion.VERSION2)


mqttc.username_pw_set(settings.mqtt_user, settings.mqtt_password.get_secret_value())
mqttc.connect(settings.mqtt_host, settings.mqtt_port, 60)
