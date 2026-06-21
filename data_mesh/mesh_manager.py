import json
import os

class MeshManager:
    def __init__(self, storage="mesh_registry.json"):
        self.storage = storage
        self.domains = self._load()

    def _load(self):
        if os.path.exists(self.storage):
            with open(self.storage) as f:
                return json.load(f)
        return {}

    def save(self):
        with open(self.storage, 'w') as f:
            json.dump(self.domains, f)

    def register_domain(self, name, owner, schema, endpoint):
        self.domains[name] = {
            'owner': owner,
            'schema': schema,
            'endpoint': endpoint
        }
        self.save()

    def query_mesh(self, sql):
        # Basit: her domain endpoint'ine HTTP sorgusu gönderip birleştir
        # Gerçekte Presto/Trino benzeri olabilir
        import requests
        results = []
        for name, info in self.domains.items():
            resp = requests.post(info['endpoint'], json={'query': sql})
            if resp.status_code == 200:
                results.append(pd.DataFrame(resp.json()['data']))
        return pd.concat(results, ignore_index=True) if results else pd.DataFrame()