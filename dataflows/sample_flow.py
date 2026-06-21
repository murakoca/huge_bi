import pandas as pd
from connectors.sql_connector import SQLConnector
from power_query.transformer import Transformer

def load_sales():
    conn = SQLConnector('sqlite:///sales.db')
    df = conn.get_data("SELECT * FROM Sales")
    print(f"Satış verisi yüklendi: {len(df)} satır")
    return df

def clean_sales(df):
    return Transformer.filter_rows(df, "Sales > 0")

def load_customers():
    conn = SQLConnector('sqlite:///sales.db')
    df = conn.get_data("SELECT * FROM Customers")
    print(f"Müşteri verisi yüklendi: {len(df)} satır")
    return df

def merge_data(sales, customers):
    merged = Transformer.merge_tables(sales, customers, on='CustomerID')
    print(f"Birleştirilmiş veri: {len(merged)} satır")
    return merged

def build_flow():
    dag = DataflowDAG()
    # Bağımsız adımlar
    dag.add_step('load_sales', load_sales)
    dag.add_step('clean_sales', clean_sales, depends_on=['load_sales'])
    dag.add_step('load_customers', load_customers)
    dag.add_step('merge_data', merge_data, depends_on=['clean_sales', 'load_customers'])
    return dag