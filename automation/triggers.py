import time
from threading import Thread
from datetime import datetime

class TriggerEngine:
    def __init__(self):
        self.triggers = []
        self.running = False

    def add_time_trigger(self, name, cron_expression, action, **kwargs):
        # Basit: belirli bir saatte tetiklenir (cron şimdilik saat:dakika formatında)
        self.triggers.append({
            'type': 'time',
            'name': name,
            'cron': cron_expression,  # "HH:MM"
            'action': action,
            'kwargs': kwargs
        })

    def add_data_trigger(self, name, condition_sql, action, model, check_interval=60):
        self.triggers.append({
            'type': 'data',
            'name': name,
            'condition_sql': condition_sql,
            'action': action,
            'model': model,
            'interval': check_interval,
            'kwargs': {}
        })

    def start(self):
        self.running = True
        def time_loop():
            while self.running:
                now = datetime.now().strftime("%H:%M")
                for t in self.triggers:
                    if t['type'] == 'time' and t['cron'] == now:
                        t['action'](**t['kwargs'])
                time.sleep(30)  # dakikada iki kez kontrol
        Thread(target=time_loop, daemon=True).start()

        def data_loop():
            while self.running:
                for t in self.triggers:
                    if t['type'] == 'data':
                        try:
                            df = t['model'].query(t['condition_sql'])
                            if not df.empty:
                                t['action'](df, **t['kwargs'])
                        except Exception as e:
                            print(f"Data trigger error: {e}")
                time.sleep(max(t.get('interval',60) for t in self.triggers if t['type']=='data') or 60)
        Thread(target=data_loop, daemon=True).start()

    def stop(self):
        self.running = False