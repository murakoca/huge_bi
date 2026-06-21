import paho.mqtt.client as mqtt
import json
import threading
from datetime import datetime

class IoTListener:
    def __init__(self, broker, port, topic, on_message_callback):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.callback = on_message_callback
        self.client = mqtt.Client()
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.thread = threading.Thread(target=self._run, daemon=True)

    def _on_connect(self, client, userdata, flags, rc):
        print(f"MQTT bağlandı, sonuç kodu {rc}")
        client.subscribe(self.topic)

    def _on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload)
            self.callback(payload)
        except Exception as e:
            print(f"Mesaj işlenemedi: {e}")

    def _run(self):
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_forever()

    def start(self):
        self.thread.start()