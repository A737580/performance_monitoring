from nicegui import ui

class KPICard:
    def __init__(self, title: str, value: str, subtitle: str, accent_color: str):
        with ui.card().classes('w-[280px] h-[120px] shadow-md rounded-2xl flex flex-col justify-center items-center'):
            ui.label(title).classes('text-base font-semibold text-gray-700')
            ui.label(value).classes(f'text-3xl font-bold text-{accent_color}-500')
            ui.label(subtitle).classes('text-sm text-gray-500')
