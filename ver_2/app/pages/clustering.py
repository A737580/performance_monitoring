from nicegui import ui
from core.layout import PageLayout
from components.nav import MobileNav

def show():
    layout = PageLayout("Кластеризация смен")

    with layout.content:
        ui.label("🧩 Кластеризация смен").classes("text-2xl font-semibold text-gray-800")
        ui.label("Визуализация кластеров появится здесь.").classes("text-gray-500 italic")

    MobileNav()
