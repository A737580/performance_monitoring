from nicegui import ui
import plotly.graph_objects as go
from .base_chart import BaseChart

class ScatterChart(BaseChart):
    def __init__(self, title: str = "Scatter Plot", x_label: str = "X", y_label: str = "Y", color_label: str = "Group"):
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.color_label = color_label

    def render(self, data: dict):
        """
        data = {
            "x": [...],
            "y": [...],
            "color": [...]  # опционально: метки кластеров или категории
        }
        """
        fig = go.Figure()

        if "color" in data:
            # Цвет по категориям (например, кластеры)
            fig.add_trace(go.Scatter(
                x=data["x"],
                y=data["y"],
                mode='markers',
                marker=dict(
                    color=data["color"],
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title=self.color_label)
                ),
                text=[f"Cluster: {c}" for c in data.get("labels", data["color"])],
                hoverinfo="text+x+y"
            ))
        else:
            # Без цвета
            fig.add_trace(go.Scatter(
                x=data["x"],
                y=data["y"],
                mode='markers'
            ))

        fig.update_layout(
            title=self.title,
            xaxis_title=self.x_label,
            yaxis_title=self.y_label,
            height=500
        )

        with ui.card().classes('w-full'):
            ui.plotly(fig).classes('w-full')