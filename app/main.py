# app/main.py
from nicegui import ui
from core.data_generator import generate_iot_error_data
from core.data_loader import load_all_error_data
from core.clustering import clusterize_errors
from visual.dashboard import create_dashboard
from visual.trends import create_trends_tab
from visual.forecast_tab import create_forecast_tab


@ui.page('/')
def main_page():
    ui.page_title('IoT Monitoring — Dashboard')

    # --- Шапка ---
    with ui.header().classes('bg-blue-600 text-white p-4 flex justify-between items-center'):
        ui.label("Система анализа производительности").classes('text-2xl font-semibold')
        ui.label("Мониторинг станка").classes('text-sm opacity-80')

    with ui.column().classes('p-6 w-full items-center gap-8'):

        ui.label('Аналитика производственных данных').classes('text-lg font-semibold')

        # Контейнер для вкладок
        with ui.tabs().classes('w-full max-w-6xl') as tabs:
            cluster_tab = ui.tab('📊 Кластеризация')
            trend_tab = ui.tab('📈 Тренды ошибок')
            forecast_tab = ui.tab('🤖 Прогноз')

        with ui.tab_panels(tabs, value=cluster_tab).classes('w-full max-w-6xl'):
            # ---------- Вкладка 1 ----------
            with ui.tab_panel(cluster_tab):
                cluster_container = ui.column().classes('w-full items-center mt-6')

                def run_analysis():
                    ui.notify("⏳ Генерация данных...")
                    generate_iot_error_data(days=10)
                    df = load_all_error_data()
                    df_clustered, stats, _ = clusterize_errors(df, n_clusters=3)
                    ui.notify("✅ Готово! Отображаю дашборд.")
                    cluster_container.clear()
                    with cluster_container:
                        create_dashboard(df_clustered, stats)
                        ui.button('🔁 Обновить', on_click=run_analysis, color='blue')

                ui.button('▶ Сгенерировать данные и кластеризовать', on_click=run_analysis, color='blue')
                with cluster_container:
                    ui.label("Нажмите кнопку, чтобы начать анализ.").classes('text-sm opacity-70')

            # ---------- Вкладка 2 ----------
            with ui.tab_panel(trend_tab):
                create_trends_tab()

            # ---------- Вкладка 3 ----------
            with ui.tab_panel(forecast_tab):
                create_forecast_tab()

    # --- Футер ---
    with ui.footer().classes('bg-gray-100 text-gray-500 p-2 text-center text-sm'):
        ui.label("© 2025 — Система анализа производственных данных")


ui.run(title='IoT Monitoring Dashboard', reload=False)
