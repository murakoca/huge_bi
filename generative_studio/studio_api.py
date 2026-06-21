from flask import Blueprint, request, jsonify
studio_bp = Blueprint('studio', __name__, url_prefix='/studio')
@studio_bp.route('/generate', methods=['POST'])
def generate():
    return jsonify({"status": "ok"})