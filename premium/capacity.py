import psutil
import time
from flask import jsonify

class CapacityMonitor:
    @staticmethod
    def get_metrics():
        return {
            'cpu_percent': psutil.cpu_percent(),
            'memory_used': psutil.virtual_memory().used // (1024 * 1024),
            'memory_total': psutil.virtual_memory().total // (1024 * 1024),
            'disk_usage': psutil.disk_usage('/').percent
        }

# Dashboard'da bir API uç noktası olarak sunulabilir.