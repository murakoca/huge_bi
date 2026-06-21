"""
Profesyonel Dashboard Layout'u
Kenar çubuğu, navbar, KPI kartları, butonlar, sekmeler
"""
from dash import dcc, html
import dash_bootstrap_components as dbc

def create_layout(df):
    regions = df['Region'].unique()
    return dbc.Container([
        # Üst Navbar
        dbc.NavbarSimple(
            brand="MEGA BI Pro",
            brand_href="/dashboard/",
            color="primary",
            dark=True,
            children=[
                dbc.NavItem(dbc.NavLink("Anasayfa", href="/dashboard/")),
                dbc.NavItem(dbc.NavLink("Raporlar", href="#")),
                dbc.NavItem(dbc.NavLink("Ayarlar", href="#")),
            ]
        ),
        html.Br(),

        # Ana satır: Kenar Çubuğu + İçerik
        dbc.Row([
            # --- Kenar Çubuğu ---
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Kontroller"),
                    dbc.CardBody([
                        html.Label("Bölge Seçimi", className="fw-bold"),
                        dcc.Dropdown(
                            id='region-filter',
                            options=[{'label': r, 'value': r} for r in regions],
                            value=regions[0],
                            clearable=False
                        ),
                        html.Hr(),
                        html.Label("Tarih Aralığı", className="fw-bold"),
                        dcc.DatePickerRange(
                            id='date-range',
                            start_date=df['Date'].min(),
                            end_date=df['Date'].max(),
                            display_format='DD/MM/YYYY'
                        ),
                        html.Hr(),
                        html.Label("Hızlı İşlemler", className="fw-bold"),
                        dbc.Button("📊 Dashboard Üret", id="btn-generate-dashboard", color="info", className="w-100 mb-2"),
                        dbc.Button("🧠 AI Sohbet", id="btn-open-chat", color="success", className="w-100 mb-2"),
                        dbc.Button("🎤 Sesli Komut", id="btn-voice-command", color="warning", className="w-100 mb-2"),
                        dbc.Button("📥 Rapor İndir", id="btn-download-report", color="primary", className="w-100 mb-2"),
                        dbc.Button("🔍 Anomali Tespiti", id="btn-anomaly", color="danger", className="w-100"),
                    ])
                ], className="shadow-sm")
            ], width=3, style={"backgroundColor": "#f8f9fa", "padding": "20px"}),

            # --- Ana İçerik ---
            dbc.Col([
                # KPI Kartları
                dbc.Row([
                    dbc.Col(dbc.Card([dbc.CardHeader("Toplam Satış"), dbc.CardBody(html.H4(id="kpi-sales", className="text-success"))], color="light"), width=3),
                    dbc.Col(dbc.Card([dbc.CardHeader("Ort. Sipariş"), dbc.CardBody(html.H4(id="kpi-avg", className="text-info"))], color="light"), width=3),
                    dbc.Col(dbc.Card([dbc.CardHeader("Müşteri Sayısı"), dbc.CardBody(html.H4(id="kpi-customers", className="text-warning"))], color="light"), width=3),
                    dbc.Col(dbc.Card([dbc.CardHeader("Anomali Sayısı"), dbc.CardBody(html.H4(id="kpi-anomalies", className="text-danger"))], color="light"), width=3),
                ], className="mb-3"),

                # Sekmeler
                dbc.Tabs([
                    dbc.Tab(label="📈 Satış Analizi", tab_id="tab-sales",
                            children=[dcc.Graph(id='sales-bar'), dcc.Graph(id='sales-line')]),
                    dbc.Tab(label="🥧 Ürün Dağılımı", tab_id="tab-pie",
                            children=[dcc.Graph(id='pie-chart')]),
                    dbc.Tab(label="🧠 AI İçgörüler", tab_id="tab-ai",
                            children=[html.Div(id="ai-insights-content")]),
                    dbc.Tab(label="🗺️ Bölgesel Harita", tab_id="tab-map",
                            children=[dcc.Graph(id='map-chart')]),
                ], id="main-tabs", active_tab="tab-sales"),

                # Chat / Voice gizli modal
                dbc.Modal([
                    dbc.ModalHeader("AI Sohbet Asistanı"),
                    dbc.ModalBody([
                        dcc.Input(id="chat-input", type="text", placeholder="Sorunuzu yazın...", className="w-100"),
                        html.Div(id="chat-response", className="mt-3")
                    ]),
                    dbc.ModalFooter(dbc.Button("Kapat", id="close-chat", className="ms-auto"))
                ], id="chat-modal", is_open=False),

                dbc.Modal([
                    dbc.ModalHeader("Sesli Komut"),
                    dbc.ModalBody("Mikrofon dinleniyor..."),
                    dbc.ModalFooter(dbc.Button("Kapat", id="close-voice", className="ms-auto"))
                ], id="voice-modal", is_open=False),
            ], width=9)
        ]),

        # Gizli Div'ler (download vb.)
        dcc.Download(id="download-report"),
    ], fluid=True)