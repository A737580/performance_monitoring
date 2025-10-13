from nicegui import ui

class Footer:
    def __init__(self):
        pass

    def render(self):
        with ui.footer().classes('bg-gray-200 p-2 text-center text-sm text-gray-600'):
            ui.label('© 2025 Система мониторинга станка | Версия 1.0')