from functools import wraps
from flask import session, abort

# Basit roller ve izinler
ROLES = {
    'admin': ['view', 'edit', 'delete', 'share', 'manage_users'],
    'editor': ['view', 'edit', 'share'],
    'viewer': ['view']
}

def require_permission(permission):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            user_role = session.get('role', 'viewer')
            allowed = ROLES.get(user_role, [])
            if permission not in allowed:
                abort(403)
            return f(*args, **kwargs)
        return decorated
    return decorator

# Kullanımı:
# @require_permission('edit')
# def some_route(): ...