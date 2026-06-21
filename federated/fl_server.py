from flask import Blueprint, request, jsonify
import numpy as np

fl_bp = Blueprint('federated', __name__, url_prefix='/federated')

# Basit ortalama federasyonu
global_model = None  # Örn. ortalama vektör

@fl_bp.route('/update', methods=['POST'])
def update():
    global global_model
    client_update = np.array(request.json['weights'])
    n = request.json['n']  # örnek sayısı
    if global_model is None:
        global_model = client_update
    else:
        # Federated averaging
        global_model = (global_model + client_update) / 2  # basit
    return jsonify({"status": "ok"})

@fl_bp.route('/model', methods=['GET'])
def get_model():
    if global_model is not None:
        return jsonify({"weights": global_model.tolist()})
    return jsonify({"error": "Model yok"}), 404