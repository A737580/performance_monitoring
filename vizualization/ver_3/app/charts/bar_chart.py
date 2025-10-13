from nicegui import ui
import plotly.graph_objects as go
from .base_chart import BaseChart

class BarChart(BaseChart):
    def __init__(self, title: str = "Bar Chart", x_label: str = "Category", y_label: str = "Value"):
        self.title = title
        self.x_label = x_label
        self.y_label = y_label

    def render(self, data: dict):
        """
        data = {
            "x": [...],   # категории (даты, месяцы, коды ошибок)
            "y": [...]    # значения
        }
        """
        fig = go.Figure(data=go.Bar(
            x=data["x"],
            y=data["y"],
            marker_color='steelblue'
        ))

        fig.update_layout(
            title=self.title,
            xaxis_title=self.x_label,
            yaxis_title=self.y_label,
            height=500
        )

        with ui.card().classes('w-full'):
            ui.plotly(fig).classes('w-full')