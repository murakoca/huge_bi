import json
import os
from collections import defaultdict

class UserBehaviorTracker:
    def __init__(self, user_id, storage_file="user_behavior.json"):
        self.user_id = user_id
        self.storage = storage_file
        self.data = self._load()

    def _load(self):
        if os.path.exists(self.storage):
            with open(self.storage) as f:
                all_data = json.load(f)
                return all_data.get(self.user_id, {"clicks": defaultdict(int), "views": defaultdict(int)})
        return {"clicks": defaultdict(int), "views": defaultdict(int)}

    def save(self):
        all_data = {}
        if os.path.exists(self.storage):
            with open(self.storage) as f:
                all_data = json.load(f)
        all_data[self.user_id] = self.data
        with open(self.storage, 'w') as f:
            json.dump(all_data, f)

    def record_click(self, element):
        self.data["clicks"][element] += 1
        self.save()

    def record_view(self, element):
        self.data["views"][element] += 1
        self.save()

    def get_top_interests(self, top_n=3):
        combined = defaultdict(int)
        for k, v in self.data["clicks"].items():
            combined[k] += v
        for k, v in self.data["views"].items():
            combined[k] += v
        return sorted(combined, key=combined.get, reverse=True)[:top_n]