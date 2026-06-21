from flask import Blueprint, request, jsonify
import pandas as pd
from model.semantic_model import SemanticModel

xmla_bp = Blueprint('xmla', __name__, url_prefix='/xmla')

# Uygulama başlatılırken model nesnesini enjekte edeceğiz
_model = None

def init_xmla(model: SemanticModel):
    global _model
    _model = model

@xmla_bp.route('/query', methods=['POST'])
def execute_query():
    if not _model:
        return jsonify({'error': 'Model not initialized'}), 500

    data = request.get_json()
    dax_query = data.get('query', '')
    # Son derece basit: "EVALUATE Sales" -> SELECT * FROM Sales
    # Gerçek bir çevirici yazılabilir.
    try:
        # Örnek: DAX'ta EVALUATE komutunu SQL'e çevirme
        if dax_query.strip().upper().startswith('EVALUATE'):
            table_name = dax_query.strip().split()[1]
            sql = f"SELECT * FROM {table_name}"
        else:
            sql = dax_query  # direkt SQL kabul edelim
        df = _model.query(sql)
        return jsonify({'result': df.to_dict(orient='records')})
    except Exception as e:
        return jsonify({'error': str(e)}), 400