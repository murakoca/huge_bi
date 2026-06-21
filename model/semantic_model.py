import duckdb
import pandas as pd

class SemanticModel:
    def __init__(self):
        self.conn = duckdb.connect(':memory:')

    def load_table(self, name, df):
        self.conn.register(name, df)

    def add_relationship(self, fact_table, fact_key, dim_table, dim_key):
        # İlişkileri meta veri olarak tutuyoruz, sorguları kendimiz yönetiyoruz.
        self.conn.execute(f"CREATE OR REPLACE VIEW {fact_table}_with_{dim_table} AS "
                          f"SELECT f.*, d.* EXCLUDE({dim_key}) "
                          f"FROM {fact_table} f JOIN {dim_table} d ON f.{fact_key} = d.{dim_key}")
        # Alternatif: direkt birleştirilmiş view oluştur.

    def query(self, sql):
        return self.conn.execute(sql).df()