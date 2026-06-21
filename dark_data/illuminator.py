import os
import pandas as pd

def find_dark_data(model):
    """
    Hiç kullanılmamış (karanlık) tabloları tespit eder.
    Kullanım günlüğü 'usage_log.csv' dosyasına yazıldığı varsayılır.
    """
    usage_log = pd.read_csv('usage_log.csv') if os.path.exists('usage_log.csv') else pd.DataFrame()
    all_tables = getattr(model, 'tables', {}).keys()
    if not isinstance(all_tables, list):
        all_tables = list(all_tables)
    dark_tables = [t for t in all_tables if 'table' not in usage_log.columns or t not in usage_log['table'].values]
    return dark_tables