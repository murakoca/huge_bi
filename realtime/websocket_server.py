from flask_socketio import SocketIO, emit
import time
import threading
import random
import pandas as pd

socketio = SocketIO(cors_allowed_origins="*")

def start_stream(app):
    socketio.init_app(app)

    def background_thread():
        """Her saniye rastgele satış verisi gönderir."""
        while True:
            data = {
                'product': random.choice(['Laptop','Phone','Tablet']),
                'sales': random.randint(1, 100),
                'timestamp': pd.Timestamp.now().isoformat()
            }
            socketio.emit('new_sale', data, namespace='/live')
            time.sleep(1)

    @socketio.on('connect', namespace='/live')
    def handle_connect():
        print('Client connected')
        # Arka plan işlemini başlat
        if not hasattr(socketio, 'thread_started'):
            socketio.thread_started = True
            t = threading.Thread(target=background_thread)
            t.daemon = True
            t.start()

@socketio.on('disconnect', namespace='/live')
def handle_disconnect():
    print('Client disconnected')