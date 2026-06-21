import pandas as pd
from model.semantic_model import SemanticModel

class AdvancedDAX:
    def __init__(self, model):
        self.model = model  # DuckDB bağlantısını tutan SemanticModel

    # --- Zaman Zekası (tam liste) ---
    def totalmtd(self, df, date_col, value_col):
        return self.model.query(f"""
            SELECT SUM({value_col}) AS MTD
            FROM df
            WHERE strftime('%Y-%m', {date_col}) = strftime('%Y-%m', CURRENT_DATE)
              AND {date_col} <= CURRENT_DATE
        """).iloc[0,0]

    def previousmonth(self, df, date_col, value_col):
        return self.model.query(f"""
            WITH last_month AS (
                SELECT MAX(strftime('%Y-%m', {date_col})) AS m
                FROM df
                WHERE {date_col} < date_trunc('month', CURRENT_DATE)
            )
            SELECT SUM({value_col})
            FROM df, last_month
            WHERE strftime('%Y-%m', {date_col}) = last_month.m
        """).iloc[0,0]

    def parallelperiod(self, df, date_col, value_col, months_back=12):
        # Basit: belirtilen ay kadar geri git
        return self.model.query(f"""
            SELECT SUM({value_col})
            FROM df
            WHERE {date_col} BETWEEN date_trunc('month', CURRENT_DATE - INTERVAL {months_back} MONTH)
                                 AND date_trunc('month', CURRENT_DATE - INTERVAL {months_back} MONTH) + INTERVAL 1 MONTH - INTERVAL 1 DAY
        """).iloc[0,0]

    # --- WINDOW, OFFSET, INDEX (DuckDB SQL) ---
    def window_sum(self, df, partition_col, order_col, value_col):
        return self.model.query(f"""
            SELECT *,
                   SUM({value_col}) OVER (PARTITION BY {partition_col} ORDER BY {order_col} ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total
            FROM df
        """)

    def offset(self, df, order_col, value_col, offset_count=1):
        return self.model.query(f"""
            SELECT *,
                   LAG({value_col}, {offset_count}) OVER (ORDER BY {order_col}) AS prev_value
            FROM df
        """)

    def index(self, df, order_col, partition_col=None):
        part = f"PARTITION BY {partition_col}" if partition_col else ""
        return self.model.query(f"""
            SELECT *,
                   ROW_NUMBER() OVER ({part} ORDER BY {order_col}) AS idx
            FROM df
        """)