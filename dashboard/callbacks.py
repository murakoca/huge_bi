from dash import Input, Output, State, dcc
import plotly.express as px
import pandas as pd
import base64
import io

def register_callbacks(app, model, chat_bi, designer, t2i):

    # --- MODAL AÇ/KAPAT ---
    @app.callback(
        Output("source-modal", "is_open"),
        Input("open-source-modal", "n_clicks"),
        prevent_initial_call=True
    )
    def toggle_source_modal(n):
        return True

    @app.callback(
        Output("chat-modal", "is_open"),
        Input("btn-chat", "n_clicks"),
        Input("close-chat", "n_clicks"),
        State("chat-modal", "is_open"),
        prevent_initial_call=True
    )
    def toggle_chat_modal(open_clicks, close_clicks, is_open):
        if open_clicks or close_clicks:
            return not is_open
        return is_open

    # --- VERİ KAYNAĞI BAĞLAMA ---
    @app.callback(
        Output('connection-status', 'children'),
        Output('data-source-store', 'data'),
        Input('btn-connect-source', 'n_clicks'),
        State('upload-file', 'contents'),
        State('upload-file', 'filename'),
        State('db-connection-string', 'value'),
        State('db-query', 'value'),
        State('api-url', 'value'),
        State('api-token', 'value'),
        prevent_initial_call=True
    )
    def connect_source(n, file_content, filename, db_conn, db_query, api_url, api_token):
        try:
            if file_content:
                content_type, content_string = file_content.split(',')
                decoded = base64.b64decode(content_string)
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8'))) if filename.endswith('.csv') else pd.read_excel(io.BytesIO(decoded))
                model.load_table('SourceData', df)
                return f"✅ {filename} yüklendi ({len(df)} satır)", {'table': 'SourceData'}
            elif db_conn:
                from connectors.sql_connector import SQLConnector
                conn = SQLConnector(db_conn)
                df = conn.get_data(db_query or "SELECT * FROM Sales")
                model.load_table('SourceData', df)
                return f"✅ Veritabanı bağlandı ({len(df)} satır)", {'table': 'SourceData'}
            elif api_url:
                import requests
                headers = {'Authorization': f'Bearer {api_token}'} if api_token else {}
                df = pd.DataFrame(requests.get(api_url, headers=headers).json())
                model.load_table('SourceData', df)
                return f"✅ API verisi alındı ({len(df)} satır)", {'table': 'SourceData'}
            return "ℹ️ Demo veri kullanılıyor", {'table': 'Sales_with_Customers'}
        except Exception as e:
            return f"❌ Hata: {str(e)}", {'table': 'Sales_with_Customers'}

    # --- DASHBOARD YENİLEME ---
    @app.callback(
        Output('sales-bar', 'figure'),
        Output('sales-line', 'figure'),
        Output('kpi-sales', 'children'),
        Output('kpi-users', 'children'),
        Output('kpi-conversion', 'children'),
        Output('kpi-growth', 'children'),
        Input('btn-refresh', 'n_clicks'),
        State('data-source-store', 'data')
    )
    def update_dashboard(n, source_data):
        if source_data is None:
            source_data = {'table': 'Sales_with_Customers'}
        table = source_data.get('table', 'Sales_with_Customers')
        try:
            df = model.query(f"SELECT * FROM {table}")
        except Exception:
            df = pd.DataFrame()

        if df.empty:
            return {}, {}, "$0", "0", "%0", "%0"

        num_cols = df.select_dtypes(include='number').columns.tolist()
        cat_cols = df.select_dtypes(include='object').columns.tolist()

        if not num_cols:
            return {}, {}, "$0", "0", "%0", "%0"

        x = cat_cols[0] if cat_cols else df.columns[0]
        y = num_cols[0]

        bar = px.bar(df, x=x, y=y, template='plotly_dark')
        line = px.line(df, x=df.columns[0], y=y, template='plotly_dark')

        kpi_sales = f"${df[y].sum():,.0f}"
        kpi_users = str(df[x].nunique())
        kpi_conv = f"%{df[y].mean():.1f}"
        kpi_growth = f"%{df[y].pct_change().mean()*100:.1f}"

        return bar, line, kpi_sales, kpi_users, kpi_conv, kpi_growth

    # --- DASHBOARD ÜRET (LLM) ---
    @app.callback(
        Output('ai-insights-content', 'children'),
        Input('btn-generate', 'n_clicks'),
        State('data-source-store', 'data'),
        prevent_initial_call=True
    )
    def generate_dashboard(n, source_data):
        table = source_data.get('table', 'Sales_with_Customers') if source_data else 'Sales_with_Customers'
        try:
            df = model.query(f"SELECT * FROM {table}")
            schema = {
                'columns': df.columns.tolist(),
                'types': {c: 'numeric' if pd.api.types.is_numeric_dtype(df[c]) else 'categorical' for c in df.columns}
            }
            plan = designer.generate_layout(f"Create a sales dashboard for the table '{table}'", schema)
            from generative_dashboard.layout_builder import LayoutBuilder
            return LayoutBuilder.build(plan, model)
        except Exception as e:
            return f"Hata: {str(e)}"

    # --- AI SOHBET ---
    @app.callback(
        Output('chat-response', 'children'),
        Input('chat-input', 'n_submit'),
        State('chat-input', 'value'),
        prevent_initial_call=True
    )
    def send_chat(n_submit, message):
        if not message:
            return "Lütfen bir soru yazın."
        result = chat_bi.process(message)
        return result.get('reply', 'Cevap alınamadı.')

    # --- RAPOR İNDİR ---
    @app.callback(
        Output('download-report', 'data'),
        Input('btn-download', 'n_clicks'),
        State('data-source-store', 'data'),
        prevent_initial_call=True
    )
    def download_report(n, source_data):
        table = source_data.get('table', 'Sales_with_Customers') if source_data else 'Sales_with_Customers'
        df = model.query(f"SELECT * FROM {table}")
        return dcc.send_data_frame(df.to_csv, "rapor.csv")