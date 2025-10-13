from nicegui import ui
from pages.dashboard import dashboard_page

@ui.page("/")
def index():
    dashboard_page()

ui.run(title="AI Performance Monitor", favicon="💡")
