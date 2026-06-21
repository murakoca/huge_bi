from flask import Blueprint, request, jsonify
chat_bp = Blueprint('chat', __name__, url_prefix='/chat')
chat_bi = None
model = None
@chat_bp.route('/message', methods=['POST'])
def handle_message():
    user_msg = request.json.get('message')
    result = chat_bi.process(user_msg)
    return jsonify({'reply': result.get('reply', '')})