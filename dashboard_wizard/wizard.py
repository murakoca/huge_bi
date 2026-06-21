from ai.chart_recommender import ChartRecommender
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.express as px

class DashboardWizard:
    def __init__(self):
        self.recommender = ChartRecommender()

    def suggest_dashboard(self, df, title="Otomatik Dashboard"):
        """
        DataFrame'i analiz eder ve Dash layout'u olarak bir div döndürür.
        """
        recommendations = self.recommender.recommend(df)[:4]  # en fazla 4 grafik
        rows = []
        for i, rec in enumerate(recommendations):
            chart_type = rec['chart_type']
            if chart_type == 'bar':
                fig = px.bar(df, x=rec['x'], y=rec['y'])
            elif chart_type == 'line':
                fig = px.line(df, x=rec['x'], y=rec['y'])
            elif chart_type == 'pie':
                fig = px.pie(df, names=rec['names'], values=rec['values'])
            elif chart_type == 'scatter':
                fig = px.scatter(df, x=rec['x'], y=rec['y'])
            else:
                fig = px.histogram(df, x=rec['x'])
            rows.append(dbc.Col(dcc.Graph(figure=fig), width=6))
            if i % 2 == 1:  # her iki grafikte bir satır ekle
                rows.append(dbc.Row(rows[-2:]))
                rows = []
        if rows:
            rows = [dbc.Row(rows)]
        return html.Div([
            html.H3(title),
            *rows
        ])