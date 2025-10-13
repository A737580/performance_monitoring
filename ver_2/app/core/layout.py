from nicegui import ui

class Header:
    def __init__(self):
        with ui.header().classes('bg-gray-50 shadow-sm h-[80px] justify-between items-center px-6'):
            with ui.row().classes('items-center gap-2'):
                ui.icon('precision_manufacturing', color='blue', size='32px')
                ui.label('AI Performance Monitor').classes('text-2xl font-bold text-gray-800')
            with ui.row().classes('items-center gap-4'):
                ui.icon('settings', size='24px').props('clickable')
                ui.icon('refresh', size='24px').props('clickable')
                ui.icon('dark_mode', size='24px').props('clickable')


class Footer:
    def __init__(self):
        with ui.footer().classes('bg-gray-800 text-white text-sm justify-between px-6 h-[60px]'):
            ui.label('© AI Performance Monitor 2025')
            ui.label('Разработка: Твой Никнейм')


class PageLayout:
    """Базовый шаблон страницы"""
    def __init__(self, title: str):
        Header()
        self.content = ui.column().classes('p-6 gap-6 w-full max-w-[1400px] mx-auto')
        Footer()
