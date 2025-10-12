# app/main.py
from nicegui import ui
from core.data_generator import generate_iot_error_data
from core.data_loader import load_all_error_data
from core.clustering import clusterize_errors
from visual.dashboard import create_dashboard


@ui.page('/')
def main_page():
    ui.page_title('IoT Monitoring — Dashboard')

    # --- ВЕРХНЕЕ МЕНЮ ---
    with ui.header().classes('bg-blue-600 text-white p-4 flex justify-between items-center'):
        ui.label("Система анализа производительности").classes('text-2xl font-semibold')
        ui.label("Мониторинг станка").classes('text-sm opacity-80')

    # --- ОСНОВНОЙ КОНТЕНТ ---
    with ui.column().classes('p-6 w-full items-center gap-8'):
        ui.label('Подготовка данных для анализа').classes('text-lg font-semibold')
        ui.label('Нажмите кнопку, чтобы сгенерировать тестовые данные и запустить кластеризацию.').classes('text-sm opacity-70')

        # Создаём контейнер, в котором будем показывать дашборд
        dashboard_container = ui.column().classes('w-full items-center mt-6')

        def run_analysis():
            ui.notify("⏳ Генерация данных...")
            generate_iot_error_data(days=10)
            df = load_all_error_data()
            df_clustered, stats, _ = clusterize_errors(df, n_clusters=3)
            ui.notify("✅ Данные готовы! Отображаю графики.")

            # очищаем контейнер и рисуем заново
            dashboard_container.clear()
            with dashboard_container:
                create_dashboard(df_clustered, stats)

        ui.button(
            'Сгенерировать и показать дашборд',
            on_click=run_analysis,
            color='blue',
            icon='play_circle'
        )

    # --- ФУТЕР ---
    with ui.footer().classes('bg-gray-100 text-gray-500 p-2 text-center text-sm'):
        ui.label("© 2025 — Система анализа производственных данных")


ui.run(title='IoT Monitoring Dashboard', reload=False)
