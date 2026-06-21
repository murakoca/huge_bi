import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.express as px
import pandas as pd

from flask import Flask, request
from flask_login import LoginManager, login_required, current_user
from flask_socketio import SocketIO

from connectors.sql_connector import SQLConnector
from model.semantic_model import SemanticModel
from power_query.transformer import Transformer
from dashboard.layouts import create_layout
from dashboard.callbacks import register_callbacks
from security.rls import apply_rls
from collaboration.comments import add_comment, get_comments
from ai.insights import anomaly_detection, smart_narrative
from dax_engine.functions import sumx, averagex
from dax_engine.advanced_dax import AdvancedDAX

from realtime.websocket_server import socketio, start_stream
from service.publish import publish_bp
from auth.models import init_db, create_user, verify_user
from auth.auth import login_manager, User, login_user, logout_user

# --- Veritabanı ve demo kullanıcılar ---
init_db()
create_user('admin', 'admin123', 'admin')
create_user('viewer', 'viewer123', 'viewer')

# --- Flask sunucusu (Dash için server) ---
server = Flask(__name__)
server.config['SECRET_KEY'] = 'gizli-anahtar'
login_manager.init_app(server)
socketio.init_app(server)  # WebSocket bağlantısı
start_stream(server)

# --- Dash uygulaması ---
app = dash.Dash(__name__, server=server, url_base_pathname='/dashboard/',
                external_stylesheets=[dbc.themes.BOOTSTRAP])

# --- Veri bağlantısı ve model ---
conn = SQLConnector('sqlite:///sales.db')
sales_df = conn.get_data("SELECT * FROM Sales")
customers_df = conn.get_data("SELECT * FROM Customers")

# Güvenlik: kullanıcı bölgesine göre filtrele
def get_secure_data():
    # Örnek: kullanıcının bölgesini session'dan al
    # Burada sabit 'EU' yapıyoruz; gerçek uygulamada current_user.region
    user_region = 'EU'
    return apply_rls(sales_df, 'Region', [user_region])

secure_sales = get_secure_data()

model = SemanticModel()
model.load_table('Sales', secure_sales)
model.load_table('Customers', customers_df)
model.add_relationship('Sales', 'CustomerID', 'Customers', 'CustomerID')

# Gelişmiş DAX nesnesi
adv_dax = AdvancedDAX(model)

# --- Layout ve Callbackler ---
app.layout = create_layout(secure_sales)
register_callbacks(app, model)

# --- Flask rotaları (Login / Logout) ---
@server.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_data = verify_user(username, password)
        if user_data:
            user = User(user_data['id'], user_data['username'], user_data['role'])
            login_user(user)
            return '''
                <h1>Giriş başarılı</h1>
                <a href="/dashboard/">Dashboard'a Git</a>
            '''
    return '''
        <form method="post">
            Kullanıcı: <input type="text" name="username"><br>
            Şifre: <input type="password" name="password"><br>
            <input type="submit" value="Giriş">
        </form>
    '''

@server.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Çıkış yapıldı'

# Service API'sini ekle
server.register_blueprint(publish_bp, url_prefix='/api')

# --- WebSocket için route (opsiyonel) ---
# SocketIO otomatik olarak /socket.io/ altında sunulur.

if __name__ == '__main__':
    socketio.run(server, debug=True, port=8050)