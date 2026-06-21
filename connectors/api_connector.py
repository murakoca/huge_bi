import requests
import pandas as pd

class APIConnector:
    def __init__(self, base_url, headers=None):
        self.base_url = base_url
        self.headers = headers or {}
    def get_data(self, endpoint):
        resp = requests.get(f"{self.base_url}/{endpoint}", headers=self.headers)
        resp.raise_for_status()
        return pd.DataFrame(resp.json())