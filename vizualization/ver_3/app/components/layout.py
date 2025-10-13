from nicegui import ui
from .header import Header
from .footer import Footer

class MainLayout:
    def __init__(self, tabs_content: dict):
        self.tabs_content = tabs_content
        self.header = Header()
        self.footer = Footer()

    def render(self):
        self.header.render()

        with ui.tabs().classes('w-full') as tabs:
            session_tab = ui.tab('Сессии')
            daily_tab = ui.tab('По дням')
            monthly_tab = ui.tab('По месяцам')

        with ui.tab_panels(tabs, value=session_tab).classes('w-full p-4'):
            with ui.tab_panel(session_tab):
                self.tabs_content['sessions']()
            with ui.tab_panel(daily_tab):
                self.tabs_content['daily']()
            with ui.tab_panel(monthly_tab):
                self.tabs_content['monthly']()

        self.footer.render()