from flask_socketio import SocketIO
from threading import Lock
import pandas as pd

class StreamingDataset:
    def __init__(self, name, socketio: SocketIO):
        self.name = name
        self.data = pd.DataFrame()
        self.lock = Lock()
        self.socketio = socketio

    def push_row(self, row_dict):
        with self.lock:
            self.data = pd.concat([self.data, pd.DataFrame([row_dict])], ignore_index=True)
        self.socketio.emit('stream_update', {'dataset': self.name, 'row': row_dict}, namespace='/stream')

    def get_snapshot(self):
        with self.lock:
            return self.data.copy()