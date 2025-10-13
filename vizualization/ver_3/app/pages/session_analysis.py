from nicegui import ui
from charts.line_chart import LineChart
from charts.scatter_chart import ScatterChart
from charts.heatmap_chart import HeatmapChart
scatter_data = {
    "x": [0.1, -0.2, 1.3, ...],
    "y": [0.5, 0.6, -0.4, ...],
    "color": [0, 0, 2, ...],  # cluster_id
    "labels": ["Стабильный", "Стабильный", "Аномальный", ...]
}

class SessionAnalysisPage:
    def __init__(self, data_loader):
        self.data_loader = data_loader

    def render(self):
        ui.label('Анализ сессий').classes('text-xl font-bold mb-4')
        
        # Загрузка данных
        session_data = self.data_loader.get_session_features()
        cluster_data = self.data_loader.get_session_clusters()

        # Графики
        LineChart("Аномальность сессий", "Сессия", "Reconstruction Error").render({
            "x": session_data["session_id"],
            "y": session_data["anomaly_score"]
        })

        ScatterChart("Кластеры сессий (UMAP)").render(cluster_data)
        ScatterChart("Кластеры сессий (UMAP)", "UMAP 1", "UMAP 2", "Кластер").render(scatter_data)
        HeatmapChart("Сигналы × Кластеры").render(
            self.data_loader.get_signal_cluster_heatmap()
        )