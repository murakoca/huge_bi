from flask import redirect, url_for, session
from functools import wraps
import uuid

def login_required_ad(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Gerçekte token doğrulanacak
        if 'azure_user' not in session:
            return redirect(url_for('azure_login'))
        return f(*args, **kwargs)
    return decorated

def azure_login():
    # Normalde Microsoft’a yönlendiririz.
    session['azure_user'] = {'name': 'Demo User', 'oid': str(uuid.uuid4())}
    return redirect('/dashboard/')