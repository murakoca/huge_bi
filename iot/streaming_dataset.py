from streaming.dataset import StreamingDataset

def create_iot_stream(socketio):
    dataset = StreamingDataset('iot_sensors', socketio)
    def handle_sensor_data(payload):
        row = {
            'timestamp': datetime.now().isoformat(),
            'temperature': payload.get('temp'),
            'humidity': payload.get('hum')
        }
        dataset.push_row(row)
    return dataset, handle_sensor_data