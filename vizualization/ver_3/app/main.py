from nicegui import ui
from components.layout import MainLayout
from pages.session_analysis import SessionAnalysisPage
from pages.daily_trends import DailyTrendsPage
from pages.monthly_summary import MonthlySummaryPage

# Мок-загрузчик данных (заменить на реальный)
class DataLoader:
    def get_session_features(self):
        return {"session_id": ["S1", "S2"], "anomaly_score": [0.05, 0.2]}
    def get_session_clusters(self):
        return {"x": [1, 2], "y": [3, 4], "color": [0, 1]}
    def get_daily_metrics(self):
        return {"date": ["2025-10-01", "2025-10-02"], "stable_session_ratio": [0.8, 0.6]}
    def get_monthly_metrics(self):
        return {"month": ["Окт"], "avg_stable_ratio": [0.7]}
data_loader = DataLoader()

# Регистрация табов
tabs = {
    'sessions': lambda: SessionAnalysisPage(data_loader).render(),
    'daily': lambda: DailyTrendsPage(data_loader).render(),
    'monthly': lambda: MonthlySummaryPage(data_loader).render(),
}

# Запуск
layout = MainLayout(tabs)
layout.render()

ui.run(title="Анализ производительности станка", reload=False)