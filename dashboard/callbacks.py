"""
Tüm buton, grafik ve etkileşim callback'leri
"""
from dash import Input, Output, State, callback
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

def register_callbacks(app, model, chat_bi, designer, t2i):
    # Ana grafikleri güncelle
    @app.callback(
        Output('sales-bar', 'figure'),
        Output('sales-line', 'figure'),
        Output('pie-chart', 'figure'),
        Output('kpi-sales', 'children'),
        Output('kpi-avg', 'children'),
        Output('kpi-customers', 'children'),
        Output('kpi-anomalies', 'children'),
        Input('region-filter', 'value'),
        Input('date-range', 'start_date'),
        Input('date-range', 'end_date'),
    )
    def update_all(region, start, end):
        df = model.query(f"SELECT * FROM Sales_with_Customers WHERE Region='{region}' AND Date BETWEEN '{start}' AND '{end}'")
        if df.empty:
            return {}, {}, {}, "$0", "$0", "0", "0"

        sales_bar = px.bar(df.groupby('Product')['Sales'].sum().reset_index(), x='Product', y='Sales', title='Ürün Bazında Satış')
        sales_line = px.line(df.groupby('Date')['Sales'].sum().reset_index(), x='Date', y='Sales', title='Günlük Satış Trendi')
        pie = px.pie(df, names='Product', values='Sales', title='Satış Dağılımı')

        kpi_sales = f"${df['Sales'].sum():,.0f}"
        kpi_avg = f"${df['Sales'].mean():,.0f}"
        kpi_cust = str(df['CustomerID'].nunique())
        # Basit anomali simülasyonu
        anomalies = len(df[df['Sales'] < df['Sales'].quantile(0.05)])
        kpi_anom = str(anomalies)

        return sales_bar, sales_line, pie, kpi_sales, kpi_avg, kpi_cust, kpi_anom

    # Dashboard üret butonu
    @app.callback(
        Output('ai-insights-content', 'children'),
        Input('btn-generate-dashboard', 'n_clicks'),
        State('region-filter', 'value'),
        prevent_initial_call=True
    )
    def generate_dashboard(n, region):
        prompt = f"Create a sales dashboard for region {region}"
        schema = {'columns': ['Product','Region','Sales','Quantity'], 'types': {'Sales':'numeric'}}
        plan = designer.generate_layout(prompt, schema)
        from generative_dashboard.layout_builder import LayoutBuilder
        return LayoutBuilder.build(plan, model)

    # Sohbet modalını aç/kapat
    @app.callback(
        Output('chat-modal', 'is_open'),
        Input('btn-open-chat', 'n_clicks'),
        Input('close-chat', 'n_clicks'),
        State('chat-modal', 'is_open'),
        prevent_initial_call=True
    )
    def toggle_chat(open_clicks, close_clicks, is_open):
        if open_clicks or close_clicks:
            return not is_open
        return is_open

    # Sesli komut modalını aç/kapat
    @app.callback(
        Output('voice-modal', 'is_open'),
        Input('btn-voice-command', 'n_clicks'),
        Input('close-voice', 'n_clicks'),
        State('voice-modal', 'is_open'),
        prevent_initial_call=True
    )
    def toggle_voice(open_clicks, close_clicks, is_open):
        if open_clicks or close_clicks:
            return not is_open
        return is_open

    # Chat mesaj gönderme
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

    # Rapor indirme (örnek CSV)
    @app.callback(
        Output('download-report', 'data'),
        Input('btn-download-report', 'n_clicks'),
        State('region-filter', 'value'),
        State('date-range', 'start_date'),
        State('date-range', 'end_date'),
        prevent_initial_call=True
    )
    def download_report(n, region, start, end):
        df = model.query(f"SELECT * FROM Sales_with_Customers WHERE Region='{region}' AND Date BETWEEN '{start}' AND '{end}'")
        return dcc.send_data_frame(df.to_csv, "rapor.csv", index=False)

    # Anomali vurgulama butonu
    @app.callback(
        Output('map-chart', 'figure'),
        Input('btn-anomaly', 'n_clicks'),
        State('region-filter', 'value'),
        prevent_initial_call=True
    )
    def show_anomalies(n, region):
        df = model.query(f"SELECT * FROM Sales_with_Customers WHERE Region='{region}'")
        # Basit bir scatter plot
        fig = px.scatter(df, x='Date', y='Sales', color='Sales', title='Anomali Tespiti')
        return fig