from flask import Blueprint, request, jsonify
import pandas as pd
from model.semantic_model import SemanticModel

odbc_bp = Blueprint('odbc', __name__, url_prefix='/odbc')

_model = None

def init_odbc(model):
    global _model
    _model = model

@odbc_bp.route('/query', methods=['POST'])
def query():
    sql = request.json.get('query', '')
    try:
        df = _model.query(sql)
        return jsonify({'data': df.to_dict(orient='records'), 'columns': df.columns.tolist()})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@odbc_bp.route('/tables', methods=['GET'])
def tables():
    # DuckDB'den tabloları listele
    tables = _model.conn.execute("SELECT name FROM sqlite_master WHERE type='view' OR type='table'").df()
    return jsonify(tables['name'].tolist())