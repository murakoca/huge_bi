from flask import Blueprint, request, jsonify
from causal_analysis.causal_engine import analyze_cause

causal_bp = Blueprint('causal', __name__, url_prefix='/causal')

@causal_bp.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    df = pd.DataFrame(data['data'])
    result = analyze_cause(df, data['treatment'], data['outcome'], data['graph'])
    return jsonify(result)