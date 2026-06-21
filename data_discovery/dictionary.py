import json

class DataDictionary:
    def __init__(self, storage_file="data_dictionary.json"):
        self.storage = storage_file
        self.dict = self._load()

    def _load(self):
        try:
            with open(self.storage) as f:
                return json.load(f)
        except:
            return {}

    def save(self):
        with open(self.storage, 'w') as f:
            json.dump(self.dict, f)

    def add_entry(self, table, column, description, data_type, business_terms=None):
        key = f"{table}.{column}"
        self.dict[key] = {
            "description": description,
            "data_type": data_type,
            "business_terms": business_terms or []
        }
        self.save()

    def search(self, term):
        results = {}
        for key, val in self.dict.items():
            if term.lower() in key.lower() or term.lower() in val['description'].lower():
                results[key] = val
        return results