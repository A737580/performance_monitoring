from nicegui import ui
from pages import dashboard, clustering

# Маршруты
routes = {
    '/': dashboard.show,
    '/clustering': clustering.show,
}

# Привязываем каждую страницу к маршруту
for path, page_fn in routes.items():
    ui.page(path)(page_fn)

ui.run(title="AI Performance Monitor", favicon="💡")
