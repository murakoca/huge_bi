import pandas as pd

class ExcelConnector:
    def __init__(self, filepath):
        self.filepath = filepath
    def get_data(self, sheet_name=0):
        return pd.read_excel(self.filepath, sheet_name=sheet_name)