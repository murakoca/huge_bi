import pandas as pd
import pyarrow.parquet as pq
import os
from glob import glob

class DataLakeConnector:
    def __init__(self, base_path):
        self.base_path = base_path  # örn: "./data_lake"

    def list_tables(self):
        # Klasör adları = tablo adları
        tables = [d for d in os.listdir(self.base_path) if os.path.isdir(os.path.join(self.base_path, d))]
        return tables

    def read_table(self, table_name):
        # İlgili klasördeki tüm parquet dosyalarını birleştir
        path = os.path.join(self.base_path, table_name, "*.parquet")
        files = glob(path)
        if files:
            return pd.concat([pd.read_parquet(f) for f in files], ignore_index=True)
        # Alternatif: Delta Lake
        delta_path = os.path.join(self.base_path, table_name, "_delta_log")
        if os.path.exists(delta_path):
            from delta import DeltaTable
            dt = DeltaTable(os.path.join(self.base_path, table_name))
            return dt.to_pandas()
        return pd.DataFrame()

    def register_in_model(self, model):
        for table in self.list_tables():
            df = self.read_table(table)
            model.load_table(table, df)
            print(f"Veri gölü tablosu yüklendi: {table}")