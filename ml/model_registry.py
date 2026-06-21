import joblib
import os
import json

REGISTRY_PATH = "ml_models/registry.json"
MODEL_DIR = "ml_models"

os.makedirs(MODEL_DIR, exist_ok=True)

class ModelRegistry:
    def __init__(self):
        self.registry = self._load_registry()

    def _load_registry(self):
        if os.path.exists(REGISTRY_PATH):
            with open(REGISTRY_PATH) as f:
                return json.load(f)
        return {}

    def save_registry(self):
        with open(REGISTRY_PATH, 'w') as f:
            json.dump(self.registry, f)

    def register_model(self, name, model, metadata=None):
        """Modeli diske kaydeder ve kayıt defterine ekler."""
        path = os.path.join(MODEL_DIR, f"{name}.pkl")
        joblib.dump(model, path)
        self.registry[name] = {
            'path': path,
            'metadata': metadata or {},
            'version': self.registry.get(name, {}).get('version', 0) + 1
        }
        self.save_registry()
        return self.registry[name]

    def load_model(self, name):
        entry = self.registry.get(name)
        if not entry:
            raise ValueError(f"Model '{name}' bulunamadı.")
        return joblib.load(entry['path'])

    def list_models(self):
        return list(self.registry.keys())