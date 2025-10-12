# app/visual/dashboard_full.py
from nicegui import ui
from core.data_loader import load_all_error_data
from core.clustering import clusterize_errors
from .charts import fig_errors_by_day, fig_error_code_distribution, fig_parameter_histogram, fig_scatter_clusters, fig_box_by_cluster
import pandas as pd

def create_dashboard_full():
    # main tabs container
    with ui.column().classes('p-6 w-full items-center gap-6'):
        ui.label("IoT Error Analyzer — визуализация").classes('text-2xl font-semibold')

        # Tabs
        with ui.tabs().classes('w-full max-w-7xl') as tabs:
            tab_overview = ui.tab('🏠 Overview')
            tab_trends = ui.tab('📈 Errors & Trends')
            tab_clusters = ui.tab('🧩 Clusters')
            tab_compare = ui.tab('🔍 Compare')

        with ui.tab_panels(tabs, value=tab_overview).classes('w-full max-w-7xl'):

            # ----------------- OVERVIEW -----------------
            with ui.tab_panel(tab_overview):
                df = safe_load()
                # KPI cards
                total_errors = len(df)
                avg_param = df['parameter_value'].mean() if 'parameter_value' in df.columns else 0
                cluster_count = df['cluster'].nunique() if 'cluster' in df.columns else 0

                with ui.row().classes('w-full gap-6'):
                    with ui.card().classes('p-4 flex-1'):
                        ui.label('Всего ошибок').classes('text-sm text-gray-600')
                        ui.label(f'{total_errors}').classes('text-3xl font-bold')
                    with ui.card().classes('p-4 flex-1'):
                        ui.label('Средний параметр').classes('text-sm text-gray-600')
                        ui.label(f'{avg_param:.2f}').classes('text-3xl font-bold')
                    with ui.card().classes('p-4 flex-1'):
                        ui.label('Число кластеров').classes('text-sm text-gray-600')
                        ui.label(f'{cluster_count}').classes('text-3xl font-bold')

                # large chart errors by day
                fig = fig_errors_by_day(df)
                ui.plotly(fig).classes('w-full')

                # small table latest entries
                ui.label('Последние ошибки').classes('text-lg font-medium mt-4')
                rows = df.tail(20).to_dict('records')
                # columns deduced
                cols = [{'name': c, 'label': c, 'field': c} for c in (['export_time','error_code','parameter_value','cluster'] if 'cluster' in df.columns else ['export_time','error_code','parameter_value'])]
                ui.table(columns=cols, rows=rows).classes('w-full').props('pagination="10"')

            # ----------------- TRENDS -----------------
            with ui.tab_panel(tab_trends):
                df = safe_load()
                ui.label('Error trends').classes('text-xl font-semibold')
                fig1 = fig_errors_by_day(df, days=30)
                ui.plotly(fig1).classes('w-full')
                fig2 = fig_error_code_distribution(df)
                ui.plotly(fig2).classes('w-full')
                fig3 = fig_parameter_histogram(df)
                ui.plotly(fig3).classes('w-full')

            # ----------------- CLUSTERS -----------------
            with ui.tab_panel(tab_clusters):
                df = safe_load()
                ui.label('Cluster analysis').classes('text-xl font-semibold')
                fig = fig_scatter_clusters(df)
                ui.plotly(fig).classes('w-full')
                figb = fig_box_by_cluster(df)
                ui.plotly(figb).classes('w-full')
                # cluster stats table if exists
                if 'cluster' in df.columns:
                    stats = df.groupby('cluster')['parameter_value'].agg(['count','mean','std']).reset_index()
                    cols = [{'name': c, 'label': c, 'field': c} for c in stats.columns]
                    rows = stats.to_dict('records')
                    ui.table(columns=cols, rows=rows).classes('w-full')

            # ----------------- COMPARE -----------------
            with ui.tab_panel(tab_compare):
                ui.label('Compare shifts — coming soon').classes('text-lg')

def safe_load():
    """Helper: loads data and ensures it has reasonable columns.
    Also runs clustering if clusters absent."""
    try:
        df = load_all_error_data()
    except Exception:
        df = pd.DataFrame(columns=['export_time','error_code','parameter_value'])

    # ensure parameter_value exists
    if 'parameter_value' not in df.columns:
        df['parameter_value'] = 0.0

    # ensure export_time exists
    if 'export_time' not in df.columns:
        df['export_time'] = pd.to_datetime('2025-01-01')

    # if no cluster column — try to cluster quickly
    if 'cluster' not in df.columns or df['cluster'].isna().all():
        try:
            df, _, _ = clusterize_errors(df, n_clusters=3)
        except Exception:
            # fallback: put all zeros
            df['cluster'] = 0

    return df
