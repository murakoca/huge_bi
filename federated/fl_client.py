import requests
import numpy as np

class FederatedClient:
    def __init__(self, server_url):
        self.server = server_url
    def send_update(self, local_weights, sample_count):
        requests.post(f"{self.server}/update", json={
            'weights': local_weights.tolist(),
            'n': sample_count
        })
    def get_global_model(self):
        resp = requests.get(f"{self.server}/model")
        return np.array(resp.json()['weights'])