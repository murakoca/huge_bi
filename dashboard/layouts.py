from dash import dcc, html
import dash_bootstrap_components as dbc

def create_layout(df):
    return html.Div([
        # === KENAR ÇUBUĞU ===
        html.Div([
            html.H3("MEGA BI Pro"),
            html.Hr(style={"border-color": "rgba(255,255,255,0.1)"}),
            dbc.Nav([
                dbc.NavLink("🏠 Dashboard", href="#", active=True),
                dbc.NavLink("📊 Raporlar", href="#"),
                dbc.NavLink("🧠 AI Analiz", href="#"),
                dbc.NavLink("⚙️ Veri Kaynakları", href="#", id="open-source-modal"),
                dbc.NavLink("📥 Dışa Aktar", href="#"),
            ], vertical=True, pills=True),
        ], className="sidebar"),

        # === ANA İÇERİK ===
        html.Div([
            # Hero
            html.Div([
                html.H1("Merhaba, Murat 👋", style={"color": "#fff", "fontWeight": "700"}),
                html.P("Veri dünyanın kontrolü sende. Bugünün öne çıkan içgörüleri aşağıda.", 
                       style={"color": "rgba(255,255,255,0.7)"}),
            ], style={"marginBottom": "30px"}),

            # KPI Kartları
            dbc.Row([
                dbc.Col(html.Div([
                    html.Div("Toplam Gelir", className="label"),
                    html.Div(id="kpi-sales", className="value", children="$0"),
                ], className="kpi-card"), width=3),
                dbc.Col(html.Div([
                    html.Div("Aktif Kullanıcı", className="label"),
                    html.Div(id="kpi-users", className="value", children="0"),
                ], className="kpi-card"), width=3),
                dbc.Col(html.Div([
                    html.Div("Dönüşüm Oranı", className="label"),
                    html.Div(id="kpi-conversion", className="value", children="%0"),
                ], className="kpi-card"), width=3),
                dbc.Col(html.Div([
                    html.Div("Büyüme", className="label"),
                    html.Div(id="kpi-growth", className="value", children="%0"),
                ], className="kpi-card"), width=3),
            ], className="mb-4"),

            # Filtreler
            dbc.Row([
                dbc.Col(dcc.Dropdown(id='region-filter', placeholder="Bölge seçin..."), width=3),
                dbc.Col(dcc.DatePickerRange(id='date-range', display_format='DD/MM/YYYY'), width=4),
                dbc.Col(dbc.Button("🔄 Yenile", id="btn-refresh", className="btn-premium"), width=2),
                dbc.Col(dbc.Button("📊 Dashboard Üret", id="btn-generate", className="btn-premium"), width=2),
                dbc.Col(dbc.Button("🧠 AI Sohbet", id="btn-chat", className="btn-premium"), width=2),
                dbc.Col(dbc.Button("📥 Rapor İndir", id="btn-download", className="btn-premium"), width=2),
            ], className="mb-4"),

            # Grafikler
            dbc.Row([
                dbc.Col(html.Div(dcc.Graph(id='sales-bar', config={'displayModeBar': False}), className="graph-container"), width=6),
                dbc.Col(html.Div(dcc.Graph(id='sales-line', config={'displayModeBar': False}), className="graph-container"), width=6),
            ]),

            # AI İçgörü alanı
            html.Div(id="ai-insights-content", className="mt-3"),

        ], className="main-content"),

        # === MODAL: Veri Kaynağı Bağlantısı ===
        dbc.Modal([
            dbc.ModalHeader("Veri Kaynağı Bağlantısı"),
            dbc.ModalBody([
                dcc.Tabs([
                    dcc.Tab(label='📁 Dosya', children=[
                        dcc.Upload(id='upload-file', children=html.Div('Dosyayı sürükleyin veya tıklayın'),
                                   style={'border': '2px dashed rgba(255,255,255,0.3)', 'borderRadius': '15px', 'padding': '30px', 'textAlign': 'center'}),
                        html.Div(id='file-info')
                    ]),
                    dcc.Tab(label='🗄️ Veritabanı', children=[
                        dcc.Input(id='db-connection-string', type='text', placeholder='postgresql://user:pass@localhost/db', className="w-100 mb-2"),
                        dcc.Textarea(id='db-query', placeholder='SELECT * FROM tablo', rows=3)
                    ]),
                    dcc.Tab(label='🌐 API', children=[
                        dcc.Input(id='api-url', type='text', placeholder='https://api.example.com/data', className="w-100 mb-2"),
                        dcc.Input(id='api-token', type='password', placeholder='Bearer token', className="w-100")
                    ]),
                ]),
                html.Div(id='connection-status', className="mt-3 text-center")
            ]),
            dbc.ModalFooter(dbc.Button("Bağlan", id="btn-connect-source", className="btn-premium")),
        ], id="source-modal", is_open=False, size="lg"),

        # === MODAL: AI Sohbet ===
        dbc.Modal([
            dbc.ModalHeader("AI Sohbet Asistanı"),
            dbc.ModalBody([
                dcc.Input(id="chat-input", type="text", placeholder="Sorunuzu yazın...", className="w-100"),
                html.Div(id="chat-response", className="mt-3")
            ]),
            dbc.ModalFooter(dbc.Button("Kapat", id="close-chat", className="ms-auto"))
        ], id="chat-modal", is_open=False),

        # Gizli depolar
        dcc.Store(id='data-source-store', storage_type='memory', data={'table': 'Sales_with_Customers'}),
        dcc.Download(id="download-report"),
    ])