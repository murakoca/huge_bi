import json
from threading import Thread
import time
from model.semantic_model import SemanticModel

class AlertEngine:
    def __init__(self, model: SemanticModel, check_interval=60):
        self.model = model
        self.interval = check_interval
        self.alerts = []  # {'name': ..., 'condition': ..., 'action': callable}
        self.running = False

    def add_alert(self, name, condition_sql, action):
        self.alerts.append({'name': name, 'condition_sql': condition_sql, 'action': action})

    def start(self):
        self.running = True
        def loop():
            while self.running:
                for alert in self.alerts:
                    try:
                        result = self.model.query(alert['condition_sql'])
                        if not result.empty:
                            alert['action'](result)
                    except Exception as e:
                        print(f"Uyarı hatası: {e}")
                time.sleep(self.interval)
        Thread(target=loop, daemon=True).start()

    def stop(self):
        self.running = False