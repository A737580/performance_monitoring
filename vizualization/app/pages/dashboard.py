from nicegui import ui


def dashboard_page():
    """Основная страница с тремя табами и графиками."""

    ui.label('📊 Dashboard').classes(
        'text-2xl font-semibold mb-6 text-center text-gray-800'
    )

    # Создаём вкладки
    with ui.tabs().classes('justify-center mb-4') as tabs:
        ui.tab('Overview')
        ui.tab('Analytics')
        ui.tab('Settings')

    # Контейнер для панелей вкладок
    with ui.tab_panels(tabs, value='Overview').classes('w-full'):
        # ---------- TAB 1: OVERVIEW ----------
        with ui.tab_panel('Overview').classes('p-4 flex flex-col items-center gap-6'):
            ui.label('Общий обзор показателей').classes('text-lg font-medium mb-2 text-gray-700')

            # Первый график
            with ui.card().classes('w-3/4 shadow-md p-4'):
                ui.label('📈 График 1 — Ошибки по дням').classes('text-md font-semibold mb-2')
                ui.line_plot(n=30).classes('w-full h-[300px]')

            # Второй график
            with ui.card().classes('w-3/4 shadow-md p-4'):
                ui.label('🔥 График 2 — Структура ошибок').classes('text-md font-semibold mb-2')
                ui.line_plot(n=30).classes('w-full h-[300px]')

        # ---------- TAB 2: ANALYTICS ----------
        with ui.tab_panel('Analytics').classes('p-4 flex flex-col items-center gap-6'):
            ui.label('Глубинная аналитика').classes('text-lg font-medium mb-2 text-gray-700')

            with ui.card().classes('w-3/4 shadow-md p-4'):
                ui.label('📊 График 1 — Аномалии по времени').classes('text-md font-semibold mb-2')
                ui.line_plot(n=50).classes('w-full h-[300px]')

            with ui.card().classes('w-3/4 shadow-md p-4'):
                ui.label('📊 График 2 — Индекс стабильности').classes('text-md font-semibold mb-2')
                ui.line_plot(n=50).classes('w-full h-[300px]')

        # ---------- TAB 3: SETTINGS ----------
        with ui.tab_panel('Settings').classes('p-4 flex flex-col items-center gap-6'):
            ui.label('Настройки панели').classes('text-lg font-medium mb-2 text-gray-700')

            with ui.card().classes('w-3/4 shadow-md p-4'):
                ui.label('⚙️ В разработке...').classes('text-gray-500 text-sm text-center')
