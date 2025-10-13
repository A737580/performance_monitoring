from nicegui import ui
from core.layout import PageLayout
from components.kpi_card import KPICard
from components.nav import MobileNav

def show():
    layout = PageLayout("Главная панель")

    with layout.content:
        ui.label("📊 Главная панель (Dashboard Overview)").classes("text-2xl font-semibold text-gray-800")

        # KPI блок
        with ui.row().classes("gap-4 flex-wrap justify-center"):
            KPICard("Ошибок за смену", "42", "в среднем за день", "blue")
            KPICard("Средний уровень аномалии", "0.17", "по последней неделе", "yellow")
            KPICard("Тип смены (кластер)", "Стабильная", "", "purple")

        ui.label("⏳ Здесь позже появятся графики, фильтры и аналитика...").classes("text-gray-500 italic")

    # Мобильная навигация
    MobileNav()
