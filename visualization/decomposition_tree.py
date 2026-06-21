import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def plot_decomposition_tree(df, path, value_col, color_col=None):
    """
    Plotly ile ayrıştırma ağacı oluşturur (sunburst grafik).
    path: hiyerarşi sütunlarının listesi (ör: ['Category', 'SubCategory'])
    value_col: sayısal değer sütunu
    """
    fig = px.sunburst(
        df,
        path=path,
        values=value_col,
        color=color_col if color_col else value_col,
        hover_data=[value_col]
    )
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    return fig

# Alternatif: Treemap
def plot_treemap(df, path, value_col):
    fig = px.treemap(df, path=path, values=value_col)
    return fig