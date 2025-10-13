# charts/line_chart.py
from nicegui import ui
import plotly.graph_objects as go
from .base_chart import BaseChart

class LineChart(BaseChart):
    def __init__(self, title: str, x_label: str = "X", y_label: str = "Y"):
        self.title = title
        self.x_label = x_label
        self.y_label = y_label

    def render(self,  data):
        """
        data = {"x": [...], "y": [...]}
        """
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=data["x"],
            y=data["y"],
            mode='lines+markers',
            line=dict(color='steelblue'),
            marker=dict(size=6)
        ))

        fig.update_layout(
            title=self.title,
            xaxis_title=self.x_label,
            yaxis_title=self.y_label,
            height=500,
            margin=dict(l=40, r=40, t=40, b=40)
        )

        with ui.card().classes('w-full'):
            ui.plotly(fig).classes('w-full')