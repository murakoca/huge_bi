import random
import time
from threading import Thread
from iot.mqtt_client import IoTListener

class EdgeDevice:
    def __init__(self, device_id, mqtt_broker, mqtt_port, model=None):
        self.device_id = device_id
        self.model = model  # Önceden yüklenmiş ML modeli
        self.listener = IoTListener(mqtt_broker, mqtt_port, f"device/{device_id}/in", self.on_message)
        self.output_topic = f"device/{device_id}/out"
        self.running = False

    def on_message(self, payload):
        features = payload.get('features')
        if features and self.model:
            pred = self.model.predict([features])[0]
            self.publish_prediction(pred)

    def publish_prediction(self, prediction):
        # MQTT ile sonucu yayınla (basit print)
        print(f"[{self.device_id}] Tahmin: {prediction}")

    def start(self):
        self.listener.start()

# Örnek bir edge model yükleme
# edge_device = EdgeDevice("temp_sensor_1", "mqtt.eclipseprojects.io", 1883, loaded_model)
# edge_device.start()