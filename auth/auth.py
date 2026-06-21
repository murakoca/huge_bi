from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from auth.models import verify_user

login_manager = LoginManager()

class User(UserMixin):
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    # Basitçe session'da tutuyoruz; gerçekte veritabanından çekilmeli
    pass