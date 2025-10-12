# app/main.py
from nicegui import ui
from core.data_generator import generate_iot_error_data
from visual.dashboard_full import create_dashboard_full

@ui.page('/')
def main_page():
    ui.page_title('IoT Monitoring — Dashboard')

    # header (top-level)
    with ui.header().classes('bg-blue-600 text-white p-4 flex justify-between items-center'):
        ui.label("IoT Error Analyzer").classes('text-2xl font-semibold')
        with ui.row():
            ui.button('Сгенерировать тестовые данные', on_click=lambda: generate_iot_error_data(days=10), color='white')
            ui.button('Обновить', on_click=lambda: ui.notify('Обновлено'), color='white')

    # main content: create dashboard
    create_dashboard_full()

    with ui.footer().classes('bg-gray-100 text-gray-600 p-2 text-center text-sm'):
        ui.label("© 2025 — IoT Error Analyzer")

ui.run(title='IoT Monitoring Dashboard', reload=False)
Ф