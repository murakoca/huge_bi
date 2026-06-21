import time

class Metering:
    def __init__(self):
        self.usage = {}  # user_id -> {"calls": int, "tokens": int}

    def record_call(self, user_id, tokens=1):
        if user_id not in self.usage:
            self.usage[user_id] = {"calls": 0, "tokens": 0}
        self.usage[user_id]["calls"] += 1
        self.usage[user_id]["tokens"] += tokens