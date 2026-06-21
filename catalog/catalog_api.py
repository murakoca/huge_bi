from flask import Blueprint, jsonify, request
from catalog.models import register_dataset, log_transformation, init_catalog
from catalog.lineage import generate_lineage

catalog_bp = Blueprint('catalog', __name__, url_prefix='/catalog')

@catalog_bp.route('/register', methods=['POST'])
def api_register():
    data = request.json
    register_dataset(data['name'], data['source'], str(data.get('schema', {})))
    return jsonify({"status": "ok"})

@catalog_bp.route('/lineage/<name>')
def api_lineage(name):
    return jsonify({"mermaid": generate_lineage(name)})