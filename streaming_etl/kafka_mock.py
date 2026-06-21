import redis
import json

class KafkaMock:
    def __init__(self, host='localhost', port=6379):
        self.r = redis.Redis(host=host, port=port)

    def produce(self, topic, message):
        self.r.publish(topic, json.dumps(message))

    def consume(self, topic, callback):
        pubsub = self.r.pubsub()
        pubsub.subscribe(topic)
        for msg in pubsub.listen():
            if msg['type'] == 'message':
                callback(json.loads(msg['data']))