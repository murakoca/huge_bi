from ai.nlp_query import NLProcessor  # Part 6

class VoiceCommandParser:
    def __init__(self):
        self.nlp = NLProcessor()

    def parse(self, text: str, schema: dict) -> dict:
        """
        "bölgelere göre satışları göster" → NLProcessor ile SQL ve grafik tipi
        """
        parsed = self.nlp.parse_question(text, schema)
        sql = self.nlp.generate_sql(parsed, 'Sales_with_Customers')
        # En uygun grafik türünü belirle
        if parsed.get('group_by'):
            chart_type = 'bar'  # varsayılan
        else:
            chart_type = 'kpi'
        return {'sql': sql, 'chart_type': chart_type, 'title': text}