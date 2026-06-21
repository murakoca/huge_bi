import re
from typing import Dict

class SimpleDAXParser:
    def __init__(self, model_tables: Dict[str, str]):
        self.tables = model_tables  # Tablo adı -> SQL'deki adı

    def parse(self, dax_query: str) -> str:
        dax = dax_query.strip()
        # EVALUATE <tablo> FILTER(...)
        eval_match = re.match(r'EVALUATE\s+(\w+)', dax, re.IGNORECASE)
        if not eval_match:
            raise ValueError("Sadece EVALUATE destekleniyor")
        table = eval_match.group(1)
        sql_table = self.tables.get(table, table)
        # FILTER(..., condition)
        filter_match = re.search(r'FILTER\s*\(([^,]+),\s*(.+)\)', dax, re.IGNORECASE)
        if filter_match:
            filter_expr = filter_match.group(2).strip()
            # Basit condition: 'Sales > 100'
            sql = f"SELECT * FROM {sql_table} WHERE {filter_expr}"
        else:
            sql = f"SELECT * FROM {sql_table}"
        return sql

# Örnek kullanım:
# parser = SimpleDAXParser({'Sales': 'sales_table'})
# parser.parse("EVALUATE Sales FILTER(Sales, Sales > 100)")
# -> "SELECT * FROM sales_table WHERE Sales > 100"