import os
import json
from flask import Blueprint, request, send_file, jsonify

marketplace_bp = Blueprint('marketplace', __name__, url_prefix='/marketplace')

UPLOAD_FOLDER = 'plugins/visuals'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@marketplace_bp.route('/upload', methods=['POST'])
def upload_visual():
    if 'file' not in request.files:
        return jsonify({"error": "Dosya yok"}), 400
    file = request.files['file']
    if file.filename == '' or not file.filename.endswith('.py'):
        return jsonify({"error": "Geçersiz dosya"}), 400
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    # Yeniden yükleme yapılabilir
    return jsonify({"message": "Eklenti yüklendi"}), 201

@marketplace_bp.route('/list', methods=['GET'])
def list_visuals():
    visuals = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith('.py') and f != '__init__.py']
    return jsonify(visuals)

@marketplace_bp.route('/download/<filename>')
def download_visual(filename):
    path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return jsonify({"error": "Bulunamadı"}), 404