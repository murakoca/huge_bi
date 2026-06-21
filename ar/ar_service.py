from flask import Blueprint, jsonify

ar_bp = Blueprint('ar', __name__, url_prefix='/ar')

@ar_bp.route('/viewer')
def viewer():
    return open('ar/ar_viewer.html').read()

@ar_bp.route('/data')
def ar_data():
    # Gerçek veriyi modelden al
    # Şimdilik statik
    return jsonify({"summary": "Günlük Satış: $12,450"})