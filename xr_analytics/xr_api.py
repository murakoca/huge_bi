from flask import Blueprint, send_from_directory, jsonify, current_app

xr_bp = Blueprint('xr', __name__, url_prefix='/xr')

@xr_bp.route('/')
def viewer():
    """WebXR / AR görüntüleyici sayfasını döndürür."""
    return current_app.send_static_file('xr_overlay.html')

@xr_bp.route('/data')
def data():
    """XR sahnesinde gösterilecek canlı veriyi sağlar."""
    # İleride model sorgulanarak dinamik veri alınabilir.
    return jsonify({"summary": "Günlük Satış: $12,450", "kpi": "+%5"})