from flask import Blueprint, render_template_string, request
from embedded.sso import generate_embed_token, sso_required

embed_bp = Blueprint('embed', __name__)

@embed_bp.route('/embed/<report_id>')
@sso_required
def view_embedded(report_id):
    # Basit: dashboard'u iframe içinde göster
    return render_template_string('''
        <html>
        <head><title>Gömülü Rapor</title></head>
        <body>
            <iframe src="/dashboard/?embed=true&token={{ token }}" width="100%" height="600px"></iframe>
        </body>
        </html>
    ''', token=request.args.get('token'))

@embed_bp.route('/api/generate_token', methods=['POST'])
def api_generate_token():
    data = request.get_json()
    token = generate_embed_token(data['user_id'], data['report_id'])
    return {'token': token}