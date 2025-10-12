# app/visual/trends.py
from nicegui import ui
import pandas as pd
import plotly.express as px
from core.data_loader import load_all_error_data


def create_trends_tab():
    with ui.column().classes('w-full items-center mt-6 gap-4'):
        ui.label("📈 Анализ трендов ошибок").classes('text-lg font-semibold')

        df = load_all_error_data()
        if df.empty:
            ui.label("Нет данных. Сначала запустите генерацию во вкладке 'Кластеризация'.")
            return

        # --- Добавляем фиктивную 'дату', если её нет ---
        if 'date' not in df.columns:
            # допустим, у нас 10 файлов → 10 дней
            # создаём псевдодаты от 1 до N
            df['date'] = pd.date_range(start='2025-01-01', periods=len(df), freq='h')

        # --- Анализ трендов ---
        errors_by_day = df.groupby(df['date'].dt.date).size().reset_index(name='count')
        fig1 = px.line(errors_by_day, x='date', y='count', title='Количество ошибок по дням')

        ui.plotly(fig1).classes('w-full max-w-5xl')

        # --- Гистограмма типов ошибок ---
        if 'error_type' in df.columns:
            fig2 = px.bar(df['error_type'].value_counts().reset_index(),
                          x='index', y='error_type',
                          title='Распределение типов ошибок',
                          labels={'index': 'Тип ошибки', 'error_type': 'Количество'})
            ui.plotly(fig2).classes('w-full max-w-5xl')
        else:
            ui.label("⚠️ В данных отсутствует столбец 'error_type' — пропускаем гистограмму.")
