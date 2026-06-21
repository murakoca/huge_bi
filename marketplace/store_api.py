from flask import Blueprint, request, jsonify, send_from_directory
import os
import json

store_bp = Blueprint('store', __name__, url_prefix='/store')
UPLOAD_FOLDER = 'marketplace/sample_plugins'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ITEMS_DB = "marketplace/items.json"

def load_items():
    if os.path.exists(ITEMS_DB):
        with open(ITEMS_DB) as f:
            return json.load(f)
    return []

def save_items(items):
    with open(ITEMS_DB, 'w') as f:
        json.dump(items, f)

@store_bp.route('/items', methods=['GET'])
def list_items():
    return jsonify(load_items())

@store_bp.route('/upload', methods=['POST'])
def upload_item():
    file = request.files.get('file')
    name = request.form.get('name')
    description = request.form.get('description')
    price = request.form.get('price', '0')
    if not file or not name:
        return jsonify({"error": "Eksik bilgi"}), 400
    filename = file.filename
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    items = load_items()
    items.append({
        'id': len(items)+1,
        'name': name,
        'description': description,
        'price': float(price),
        'file': filename,
        'downloads': 0
    })
    save_items(items)
    return jsonify({"message": "Eklenti eklendi"}), 201

@store_bp.route('/download/<filename>')
def download_item(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)