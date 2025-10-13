from nicegui import ui
from core.theme import THEME


class Header:
    def __init__(self):
        with ui.header().classes(
            "bg-[#F8F8F8] shadow-sm h-[80px] flex justify-between items-center px-8"
        ):
            # Левая часть — логотип и название
            with ui.row().classes("items-center gap-3"):
                ui.icon("precision_manufacturing", color=THEME["primary"], size="32px")
                ui.label("AI Performance Monitor").classes(
                    "text-2xl font-bold text-gray-800"
                )

            # Правая часть — иконки
            with ui.row().classes("items-center gap-5"):
                ui.icon("refresh", size="24px").props("clickable")
                ui.icon("settings", size="24px").props("clickable")
                ui.icon("dark_mode", size="24px").props("clickable")


class Footer:
    def __init__(self):
        with ui.footer().classes(
            f"bg-[{THEME['footer_bg']}] text-white text-sm justify-between px-8 h-[60px] items-center"
        ):
            ui.label("© AI Performance Monitor 2025")
            ui.label("Разработка: Твой Никнейм")


class PageLayout:
    """Базовый шаблон страницы"""

    def __init__(self, title: str):
        self.title = title
        Header()
        # Контентная область по центру
        self.content = ui.column().classes(
            "min-h-[calc(100vh-140px)] p-8 bg-[#F8F8F8] items-center gap-8"
        )
        Footer()
