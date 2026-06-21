import plotly.graph_objects as go
import pandas as pd

class DigitalTwin:
    def __init__(self):
        # Basit bir fabrika yerleşimi (dikdörtgenler)
        self.layout = {
            'Makineler': {'x': [1, 3, 5], 'y': [2, 2, 2], 'durum': [1, 0, 1]},
        }

    def update_status(self, sensor_data):
        # sensör verisine göre durum güncelle
        pass

    def render_3d(self):
        fig = go.Figure()
        for name, vals in self.layout.items():
            fig.add_trace(go.Scatter3d(
                x=vals['x'], y=vals['y'], z=[0]*len(vals['x']),
                mode='markers',
                marker=dict(size=20, color=['green' if s else 'red' for s in vals['durum']]),
                name=name
            ))
        fig.update_layout(title="Fabrika Dijital İkizi")
        return fig