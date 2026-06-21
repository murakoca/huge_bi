import dash_bootstrap_components as dbc
from dash import dcc, html
import plotly.express as px

class LayoutBuilder:
    @staticmethod
    def build(plan: dict, model) -> html.Div:
        components = []
        for comp in plan['components']:
            if comp['type'] == 'kpi':
                df = model.query(comp['query'])
                value = df.iloc[0,0] if not df.empty else 0
                comp_div = dbc.Card([
                    dbc.CardHeader(comp['title']),
                    dbc.CardBody(html.H2(f"{value:,.2f}"))
                ])
            elif comp['type'] == 'bar_chart':
                df = model.query(comp['query'])
                fig = px.bar(df, x=comp['x'], y=comp['y'], title=comp['title'])
                comp_div = dcc.Graph(figure=fig)
            elif comp['type'] == 'line_chart':
                df = model.query(comp['query'])
                fig = px.line(df, x=comp['x'], y=comp['y'], title=comp['title'])
                comp_div = dcc.Graph(figure=fig)
            else:
                comp_div = html.Div(f"Bilinmeyen bileşen: {comp['type']}")
            components.append(dbc.Col(comp_div, width=6))
        # Satırlar halinde düzenle
        rows = []
        for i in range(0, len(components), 2):
            rows.append(dbc.Row(components[i:i+2]))
        return html.Div([html.H2(plan.get('title', 'Dashboard')), *rows])