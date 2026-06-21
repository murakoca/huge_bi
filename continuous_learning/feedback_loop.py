import json
import os
import time

class FeedbackCollector:
    def __init__(self, storage="feedback.json"):
        self.storage = storage

    def record(self, query, user_rating, outcome):
        entry = {
            'query': query,
            'rating': user_rating,
            'outcome': outcome,
            'timestamp': time.time()
        }
        data = []
        if os.path.exists(self.storage):
            with open(self.storage, 'r') as f:
                data = json.load(f)
        data.append(entry)
        with open(self.storage, 'w') as f:
            json.dump(data, f)

    def get_training_data(self):
        if not os.path.exists(self.storage):
            return []
        with open(self.storage, 'r') as f:
            data = json.load(f)
        return [(d['query'], d['outcome']) for d in data if d['rating'] > 3]