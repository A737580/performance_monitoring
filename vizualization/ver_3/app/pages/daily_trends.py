from nicegui import ui
from charts.line_chart import LineChart
from charts.bar_chart import BarChart

class DailyTrendsPage:
    def __init__(self, data_loader):
        self.data_loader = data_loader

    def render(self):
        ui.label('Аналитика по дням').classes('text-xl font-bold mb-4')
        
        daily = self.data_loader.get_daily_metrics()

        LineChart("Доля стабильных сессий по дням").render({
            "x": daily["date"],
            "y": daily["stable_session_ratio"]
        })

        BarChart("Количество сессий в день").render({
            "x": daily["date"],
            "y": daily["total_sessions"]
        })