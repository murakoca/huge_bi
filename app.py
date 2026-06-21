"""
MEGA BI Pro – Ana Uygulama (Temiz, Çalışan, Profesyonel Arayüz)
Ollama LLM, Dash CYBORG tema, 15 bölüm modülleri.
"""

import os
import sys
import pandas as pd
from dash import dcc
import dash_bootstrap_components as dbc

# TensorFlow gürültüsünü tamamen kapat
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# --- Flask & Dash -------------------------------------------------------------
from flask import Flask, redirect, request, jsonify, send_file, session
import dash
from flask_socketio import SocketIO

# --- İç modüller ----------------------------------------------------------------
from connectors.sql_connector import SQLConnector
from model.semantic_model import SemanticModel
from security.rls import apply_rls

from ai.report_writer import ReportWriter
from ai.insights import anomaly_detection, smart_narrative
from ai.chart_recommender import ChartRecommender
from ai.nlp_query import NLProcessor
from ai.advanced_anomaly import AdvancedAnomalyDetector
from chat_bi.bot_core import ChatBI
from generative_studio.designer import GenerativeStudio
from generative_dashboard.llm_designer import LLMDashboardDesigner
from text_to_insight.pipeline import TextToInsight

from dashboard.layouts import create_layout
from dashboard.callbacks import register_callbacks

from service.publish import publish_bp
from embedded.embed_api import embed_bp
from xmla.endpoint import xmla_bp, init_xmla
from reporting.email_distributor import send_report_email, scheduler
from collaboration.realtime_collab import socketio as collab_sio
from admin.admin_panel import admin_bp
from catalog.catalog_api import catalog_bp, init_catalog
from alerts.engine import AlertEngine
from alerts.notifier import notify_email
from streaming.dataset import StreamingDataset
from marketplace.store_api import store_bp
from ml.prediction_api import predict_bp
from ar.ar_service import ar_bp
from federated.fl_server import fl_bp
from odbc_bridge.query_server import odbc_bp, init_odbc
from digital_twin.twin_api import twin_bp
from causal_analysis.root_cause import causal_bp
from data_mesh.mesh_manager import MeshManager
from video_narrative.script_generator import generate_script
from video_narrative.video_builder import create_video
from fulltext_search.search_engine import SearchEngine
from compliance.gdpr_masker import mask_pii
from quantum_optimizer.qiskit_solver import QuantumOptimizer
from synthetic_data.generator import SMOTESynthetic
from autonomous_agent.insight_agent import InsightAgent
from time_travel.snapshot_query import TimeTravel
from sustainability.carbon_calculator import calculate_report_carbon
from voice.speech_to_text import SpeechRecognizer
from voice.command_parser import VoiceCommandParser
from biometrics.emotion_tracker import detect_emotion
from xr_analytics.xr_api import xr_bp
from self_healing_platform.health_monitor import platform_health, auto_heal
from dark_data.illuminator import find_dark_data
from continuous_learning.feedback_loop import FeedbackCollector

# --- Çevresel değişkenler -------------------------------------------------------
from dotenv import load_dotenv
load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")
SECRET_KEY = os.getenv("SECRET_KEY", "gizli-anahtar")

# --- Flask uygulaması -----------------------------------------------------------
server = Flask(__name__)
server.config['SECRET_KEY'] = SECRET_KEY
collab_sio.init_app(server)

# --- Veritabanı ve model --------------------------------------------------------
conn = SQLConnector('sqlite:///sales.db')
sales_df = conn.get_data("SELECT * FROM Sales")
customers_df = conn.get_data("SELECT * FROM Customers")
secure_sales = apply_rls(sales_df, 'Region', ['EU'])
model = SemanticModel()
model.load_table('Sales', secure_sales)
model.load_table('Customers', customers_df)
model.add_relationship('Sales', 'CustomerID', 'Customers', 'CustomerID')

init_xmla(model)
init_odbc(model)
init_catalog()

# --- AI nesneleri ---------------------------------------------------------------
report_writer = ReportWriter(ollama_url=OLLAMA_URL, model=OLLAMA_MODEL)
chat_bi = ChatBI(model=OLLAMA_MODEL, base_url=OLLAMA_URL)
studio = GenerativeStudio(ollama_url=OLLAMA_URL, model=OLLAMA_MODEL)
dashboard_designer = LLMDashboardDesigner(ollama_url=OLLAMA_URL, model=OLLAMA_MODEL)
text_to_insight = TextToInsight(model, chat_bi, report_writer)

chart_rec = ChartRecommender()
nlp = NLProcessor()
anomaly_detector = AdvancedAnomalyDetector(method='isolation_forest')

# --- Akış veri setleri (MQTT kapalı) -------------------------------------------
stream_sio = SocketIO()
stream_ds = StreamingDataset('live_sales', stream_sio)

# IoT MQTT bağlantısı yok sayılıyor
# try:
#     iot_dataset, iot_handler = create_iot_stream(stream_sio)
#     mqtt_listener = IoTListener("mqtt.eclipseprojects.io", 1883, "fabrika/sensor", iot_handler)
#     mqtt_listener.start()
# except Exception as e:
#     print(f"IoT devre dışı (MQTT): {e}")

# --- Uyarı motoru (arka planda çalışır) ----------------------------------------
alert_engine = AlertEngine(model)
alert_engine.add_alert(
    'dusuk_satis',
    "SELECT Region, SUM(Sales) as Total FROM Sales_with_Customers GROUP BY Region HAVING Total < 1000",
    lambda df: notify_email('admin@example.com', 'Düşük Satış Uyarısı', df.to_html())
)
alert_engine.start()

# --- Zamanlanmış işler -----------------------------------------------------------
from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()
scheduler.add_job(
    lambda: send_report_email("admin@company.com", "Günlük Rapor", "<h1>Satış Özeti</h1>"),
    'cron', hour=8, minute=0
)
scheduler.add_job(auto_heal, 'interval', minutes=5)
scheduler.start()

# --- Dash uygulaması (profesyonel arayüz) ---------------------------------------
app = dash.Dash(
    __name__,
    server=server,
    url_base_pathname='/dashboard/',
    external_stylesheets=[dbc.themes.CYBORG],
    suppress_callback_exceptions=True,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
)

app.layout = create_layout(secure_sales)
register_callbacks(app, model, chat_bi, dashboard_designer, text_to_insight)

# --- Flask Blueprint kayıtları --------------------------------------------------
server.register_blueprint(publish_bp, url_prefix='/api')
server.register_blueprint(embed_bp)
server.register_blueprint(xmla_bp)
server.register_blueprint(admin_bp)
server.register_blueprint(catalog_bp)
server.register_blueprint(store_bp)
server.register_blueprint(predict_bp)
server.register_blueprint(ar_bp)
server.register_blueprint(odbc_bp)
server.register_blueprint(twin_bp)
server.register_blueprint(causal_bp)
server.register_blueprint(xr_bp)

# --- Flask rotaları -------------------------------------------------------------
@server.route('/')
def index():
    return redirect('/dashboard/')

@server.route('/api/summary')
def api_summary():
    df = model.query("SELECT SUM(Sales) as total FROM Sales_with_Customers")
    total = df.iloc[0,0] if not df.empty else 0
    return jsonify({'total_sales': total})

@server.route('/api/ask')
def ask_question():
    q = request.args.get('q', '')
    schema = {'columns': ['Product','Region','Sales','Quantity'], 'types': {'Sales':'numeric'}}
    parsed = nlp.parse_question(q, schema)
    sql = nlp.generate_sql(parsed, 'Sales_with_Customers')
    df = model.query(sql)
    return jsonify({
        'result': df.to_dict(orient='records'),
        'sql': sql,
        'chart_suggestions': chart_rec.recommend(df)[:2]
    })

@server.route('/ask-insight', methods=['POST'])
def ask_insight():
    q = request.json['question']
    result = text_to_insight.process(q)
    return jsonify(result)

@server.route('/generate-dashboard', methods=['POST'])
def gen_dashboard():
    data = request.json
    schema = {'columns': ['Product','Region','Sales'], 'types': {'Sales':'numeric'}}
    plan = dashboard_designer.generate_layout(data.get('prompt', ''), schema)
    return jsonify(plan)

@server.route('/summarize', methods=['POST'])
def summarize():
    df = model.query("SELECT * FROM Sales_with_Customers LIMIT 50")
    return report_writer.summarize(df)

@server.route('/voice-command', methods=['POST'])
def voice_command():
    text = request.json.get('text', '')
    if not text:
        sr = SpeechRecognizer()
        text = sr.listen_and_convert()
    parser = VoiceCommandParser()
    cmd = parser.parse(text, {'columns': ['Product','Region','Sales'], 'types': {'Sales':'numeric'}})
    df = model.query(cmd['sql'])
    return jsonify({'command': cmd, 'data_preview': df.head().to_dict()})

@server.route('/what-if', methods=['POST'])
def what_if():
    from what_if.simulator import MonteCarloSimulator
    def profit(params): return params['price'] * params['volume'] - params['cost']
    sim = MonteCarloSimulator(profit, {
        'price': ('normal', (100, 5)),
        'volume': ('normal', (1000, 50)),
        'cost': ('uniform', (20000, 30000))
    }, num_simulations=500)
    return jsonify(sim.run())

@server.route('/avatar-video')
def avatar_video():
    script = ["Satışlar bu çeyrekte %20 arttı.", "En çok satan ürün Laptop oldu."]
    path = create_video(script, avatar_image_path="static/avatar.png", output="static/avatar_report.mp4")
    return send_file(path, as_attachment=True)

@server.route('/health')
def health():
    return jsonify(platform_health())

@server.route('/dark-data')
def dark_data():
    return jsonify(find_dark_data(model))

@server.route('/search')
def search():
    q = request.args.get('q', '')
    se = SearchEngine()
    return jsonify(se.search(q))

@server.route('/gdpr/export')
def gdpr_export():
    df = model.query("SELECT * FROM Customers")
    masked = mask_pii(df, ['CustomerName'])
    return masked.to_csv(index=False)

# --- Ana çalıştırma -------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)