from nicegui import ui

class MobileNav:
    def __init__(self):
        with ui.footer().classes('bg-white border-t fixed bottom-0 w-full lg:hidden'):
            with ui.row().classes('justify-around w-full'):
                ui.button('🏠', on_click=lambda: ui.open('/')).props('flat')
                ui.button('🧩', on_click=lambda: ui.open('/clustering')).props('flat')
                ui.button('🚨', on_click=lambda: ui.open('/anomalies')).props('flat')
                ui.button('📊', on_click=lambda: ui.open('/reports')).props('flat')
