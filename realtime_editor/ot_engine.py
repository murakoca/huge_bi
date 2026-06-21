import difflib

class OTEngine:
    """
    Basit Operasyonel Dönüşüm motoru.
    Her düzenleme: {position, delete_count, insert_text}
    """
    @staticmethod
    def apply(document: str, operation: dict) -> str:
        pos = operation['position']
        del_count = operation.get('delete_count', 0)
        insert = operation.get('insert_text', '')
        new_doc = document[:pos] + document[pos+del_count:]
        new_doc = new_doc[:pos] + insert + new_doc[pos:]
        return new_doc

    @staticmethod
    def transform(op1, op2):
        """İki eşzamanlı operasyonu birbirine göre dönüştürür."""
        # Basit: operasyon sıralamasına göre pozisyonları kaydır
        if op1['position'] >= op2['position']:
            op1['position'] += len(op2.get('insert_text', '')) - op2.get('delete_count', 0)
        return op1

    @staticmethod
    def merge(document: str, ops: list) -> str:
        for op in sorted(ops, key=lambda x: x['position']):
            document = OTEngine.apply(document, op)
        return document