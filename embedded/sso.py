from flask import request, redirect, url_for, session
from functools import wraps
import jwt
import uuid

SECRET_KEY = "gömülü-sso-gizli"

def generate_embed_token(user_id, report_id, valid_seconds=3600):
    payload = {
        'user_id': user_id,
        'report_id': report_id,
        'jti': str(uuid.uuid4()),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_embed_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except:
        return None

def sso_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return "Token gerekli", 401
        payload = verify_embed_token(token)
        if not payload:
            return "Geçersiz token", 401
        # Oturuma kullanıcıyı ekle
        session['user_id'] = payload['user_id']
        session['embed_report'] = payload['report_id']
        return f(*args, **kwargs)
    return decorated