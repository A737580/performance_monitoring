# components/header.py
from nicegui import ui

class Header:  # ← Обязательно с большой буквы!
    def render(self):
        with ui.header().classes('items-center justify-between bg-gray-800 text-white p-4'):
            ui.label('📊 Производительность станка').classes('text-2xl font-bold')
            ui.label('Анализ ошибок и предупреждений').classes('text-sm opacity-75')