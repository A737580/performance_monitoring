from nicegui import ui
import plotly.graph_objects as go
from .base_chart import BaseChart

class HeatmapChart(BaseChart):
    def __init__(self, title: str = "Heatmap", x_label: str = "X", y_label: str = "Y"):
        self.title = title
        self.x_label = x_label
        self.y_label = y_label

    def render(self, data: dict):
        """
        data = {
            "z": [[...], [...], ...],  # матрица значений
            "x": [...],               # подписи по X (например, ошибки)
            "y": [...]                # подписи по Y (например, кластеры)
        }
        """
        fig = go.Figure(data=go.Heatmap(
            z=data["z"],
            x=data["x"],
            y=data["y"],
            colorscale='Blues',
            text=data["z"],
            texttemplate="%{text:.2f}",
            textfont={"size": 10},
            hoverongaps=False
        ))

        fig.update_layout(
            title=self.title,
            xaxis_title=self.x_label,
            yaxis_title=self.y_label,
            height=500
        )

        with ui.card().classes('w-full'):
            ui.plotly(fig).classes('w-full')