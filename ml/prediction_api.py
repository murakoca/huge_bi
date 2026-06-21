from flask import Blueprint, request, jsonify
from ml.model_registry import ModelRegistry

predict_bp = Blueprint('predict', __name__, url_prefix='/predict')
registry = ModelRegistry()

@predict_bp.route('/<model_name>', methods=['POST'])
def predict(model_name):
    try:
        model = registry.load_model(model_name)
    except ValueError:
        return jsonify({'error': 'Model bulunamadı'}), 404

    data = request.get_json()
    if not data or 'features' not in data:
        return jsonify({'error': 'features gerekli'}), 400
    try:
        # Basit: features listesini 2D array olarak kabul et
        prediction = model.predict([data['features']])
        return jsonify({'prediction': prediction.tolist()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500