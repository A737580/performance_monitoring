# app/visual/dashboard.py
from nicegui import ui
import plotly.express as px
import pandas as pd

def create_dashboard(df: pd.DataFrame, cluster_stats: pd.DataFrame):
    """Создаёт визуализацию без верхнего layout (только контент)"""
    with ui.column().classes('p-6 w-full items-center gap-8'):
        ui.label("Распределение ошибок по кластерам").classes('text-xl font-semibold text-gray-800')

        # --- График 1: Scatter plot ---
        fig_scatter = px.scatter(
            df, x="parameter_value", y="export_time",
            color="cluster", title="Ошибки по дням и параметрам",
            hover_data=["error_code"]
        )
        fig_scatter.update_layout(height=500, margin=dict(l=20, r=20, t=60, b=20))
        ui.plotly(fig_scatter).classes('w-full max-w-6xl')

        # --- График 2: Box plot ---
        ui.label("Распределение значений по кластерам").classes('text-lg font-medium mt-8 text-gray-700')
        fig_box = px.box(
            df, x="cluster", y="parameter_value",
            color="cluster", points="all",
            title="Вариации параметра внутри кластеров"
        )
        fig_box.update_layout(height=400, margin=dict(l=20, r=20, t=60, b=20))
        ui.plotly(fig_box).classes('w-full max-w-5xl')

        # --- Таблица статистики ---
        ui.label("Сводная статистика по кластерам").classes('text-lg font-medium mt-10 text-gray-700')

        columns = [
            {'name': 'cluster', 'label': 'Кластер', 'field': 'cluster'},
            {'name': 'count', 'label': 'Количество записей', 'field': 'count'},
            {'name': 'mean', 'label': 'Среднее значение параметра', 'field': 'mean'},
            {'name': 'std', 'label': 'Отклонение', 'field': 'std'},
        ]

        rows = [
            {
                'cluster': int(row.cluster),
                'count': int(row['count']),
                'mean': f"{row['mean']:.2f}",
                'std': f"{row['std']:.2f}"
            }
            for _, row in cluster_stats.iterrows()
        ]

        ui.table(columns=columns, rows=rows).classes('max-w-3xl w-full')

        ui.separator()
        ui.label("© 2025 — Анализ данных производительности").classes('text-xs opacity-60 mt-6')
