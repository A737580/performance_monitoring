from nicegui import ui
from charts.bar_chart import BarChart
from charts.line_chart import LineChart

class MonthlySummaryPage:
    def __init__(self, data_loader):
        self.data_loader = data_loader

    def render(self):
        ui.label('Сводка по месяцам').classes('text-xl font-bold mb-4')
        
        monthly = self.data_loader.get_monthly_metrics()

        BarChart("Средняя доля стабильных сессий").render({
            "x": monthly["month"],
            "y": monthly["avg_stable_ratio"]
        })

        LineChart("Тренд аномальных сессий").render({
            "x": monthly["month"],
            "y": monthly["anomaly_session_ratio"]
        })