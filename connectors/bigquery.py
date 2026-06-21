import pandas as pd

class BigQueryConnector:
    def __init__(self, project_id):
        self.project_id = project_id
    def get_data(self, query):
        # google-cloud-bigquery ile sorgu
        # Simüle:
        return pd.DataFrame({'col1': [1,2], 'col2': ['a','b']})