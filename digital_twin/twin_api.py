from flask import Blueprint, jsonify
from digital_twin.twin_model import DigitalTwin

twin_bp = Blueprint('twin', __name__, url_prefix='/twin')
twin = DigitalTwin()

@twin_bp.route('/status')
def status():
    return jsonify(twin.layout)