import re

class NLProcessor:
    """
    Hafif, regex tabanlı NL işleyici.
    Anahtar kelimelerle toplama, gruplama ve sütun eşleştirme.
    """
    AGG_MAP = {
        'toplam': 'sum', 'sum': 'sum', 'total': 'sum',
        'ortalama': 'avg', 'average': 'avg',
        'say': 'count', 'count': 'count',
        'maksimum': 'max', 'max': 'max',
        'minimum': 'min', 'min': 'min'
    }

    def parse_question(self, question: str, table_schema: dict) -> dict:
        """
        Soruyu çözümler ve bir sorgu planı döndürür.
        Örnek: "bölgelere göre toplam satış" -> {'aggregation': 'sum', 'column': 'Sales', 'group_by': 'Region'}
        """
        text = question.lower().strip()
        # Toplama fonksiyonunu bul
        agg = 'sum'  # varsayılan
        for word, func in self.AGG_MAP.items():
            if word in text:
                agg = func
                break

        # Sütun ve gruplama keşfi (basit kelime eşleştirme)
        column = None
        group_by = None
        columns = table_schema.get('columns', [])
        # Sırasıyla sütun adlarını ara
        for col in columns:
            if col.lower() in text:
                if column is None:
                    column = col
                elif group_by is None:
                    group_by = col
        if column is None:
            # Sayısal sütunu varsay
            types = table_schema.get('types', {})
            for col, t in types.items():
                if t == 'numeric':
                    column = col
                    break
        return {'aggregation': agg, 'column': column, 'group_by': group_by}

    def generate_sql(self, parsed: dict, table_name: str) -> str:
        col = parsed['column'] or 'Sales'
        grp = parsed['group_by']
        agg = parsed['aggregation']
        if grp:
            return f"SELECT {grp}, {agg}({col}) AS {agg}_{col} FROM {table_name} GROUP BY {grp}"
        else:
            return f"SELECT {agg}({col}) AS {agg}_{col} FROM {table_name}"