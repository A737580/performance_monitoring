from nicegui import ui
import matplotlib.pyplot as plt
import io
import base64

def create_dashboard(df, stats):
    ui.notify('📈 Построение графиков...', type='info')

    # Таблица статистики кластеров
    ui.label('📊 Результаты кластеризации').classes('text-xl font-bold mt-4')

    rows = stats.to_dict('records')
    columns = [{'name': c, 'label': c.capitalize(), 'field': c} for c in stats.columns]

    ui.table(columns=columns, rows=rows).props('rows-per-page-options="[5,10,20]" rows-per-page="10"').classes('w-full max-w-3xl')

    # --- График распределения ---
    fig, ax = plt.subplots()
    ax.bar(stats['cluster'], stats['count'], color=['#007bff', '#ff5733', '#28a745'])
    ax.set_xlabel('Кластер')
    ax.set_ylabel('Количество записей')
    ax.set_title('Распределение по кластерам')

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    img_str = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close(fig)

    ui.image(f'data:image/png;base64,{img_str}').classes('max-w-3xl rounded-lg shadow-lg mt-4')
    ui.notify('✅ Готово: данные визуализированы!', type='positive')
