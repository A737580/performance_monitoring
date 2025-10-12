# app/visual/forecast_tab.py
from nicegui import ui

def create_forecast_tab():
    with ui.column().classes('w-full items-center mt-6 gap-4'):
        ui.label("🤖 Прогноз производственных отклонений").classes('text-lg font-semibold')
        ui.label("Раздел в разработке. Здесь появятся модели, предсказывающие сбои и эффективность оборудования.").classes('opacity-70')
        ui.button("📅 Добавить модель прогноза", color='gray', icon='brain-circuit', on_click=lambda: ui.notify("Пока в разработке!"))
