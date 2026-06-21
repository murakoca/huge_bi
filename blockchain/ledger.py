import hashlib
import json
from datetime import datetime

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data  # {"action": "report_edit", "user": "...", "details": ...}
        self.previous_hash = previous_hash
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis = Block(0, str(datetime.now()), {"action": "genesis"}, "0")
        self.chain.append(genesis)

    def add_block(self, data):
        prev = self.chain[-1]
        new_block = Block(len(self.chain), str(datetime.now()), data, prev.hash)
        self.chain.append(new_block)
        return new_block

    def verify(self):
        for i in range(1, len(self.chain)):
            if self.chain[i].hash != self.chain[i].compute_hash():
                return False
            if self.chain[i].previous_hash != self.chain[i-1].hash:
                return False
        return True