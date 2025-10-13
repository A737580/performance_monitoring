import numpy as np
import pandas as pd
import plotly.graph_objects as go
from nicegui import ui


class ChartCard:
    """Универсальный класс для отображения графика с подписью и легендой"""
    
    def __init__(self, title: str, figure):
        with ui.card().classes('w-full shadow-lg rounded-xl p-4'):
            ui.label(title).classes('text-lg font-bold mb-2')
            ui.plotly(figure).classes('w-full')


class DataGenerator:
    """Генератор тестовых данных для демонстрации"""
    
    @staticmethod
    def generate_clusters_data():
        """Данные для вкладки Обзор"""
        np.random.seed(42)
        clusters = []
        for i in range(3):
            center = np.random.uniform(0, 100, 5)
            data = np.random.normal(center, 10, (50, 5))
            for j, row in enumerate(data):
                clusters.append({
                    'cluster': i,
                    'param1': row[0],
                    'param2': row[1],
                    'param3': row[2],
                    'param4': row[3],
                    'param5': row[4]
                })
        return pd.DataFrame(clusters)
    
    @staticmethod
    def generate_timeseries_data():
        """Данные для вкладки Тренды"""
        dates = pd.date_range('2024-01-01', periods=100, freq='D')
        actual = np.cumsum(np.random.randn(100)) + 50
        predicted = actual + np.random.normal(0, 2, 100)
        return pd.DataFrame({
            'date': dates,
            'actual': actual,
            'predicted': predicted,
            'parameter': np.sin(np.arange(100) / 10) * 20 + 50
        })
    
    @staticmethod
    def generate_anomalies_data():
        """Данные для вкладки Аномалии"""
        np.random.seed(42)
        n = 200
        x = np.arange(n)
        y = 50 + np.sin(x / 20) * 10 + np.random.normal(0, 2, n)
        
        # Добавляем аномалии
        anomaly_indices = np.random.choice(n, 15, replace=False)
        y_anomaly = y.copy()
        y_anomaly[anomaly_indices] += np.random.uniform(20, 40, 15)
        
        errors = np.abs(y - y_anomaly + np.random.normal(0, 1, n))
        
        return pd.DataFrame({
            'x': x,
            'y': y_anomaly,
            'error': errors,
            'is_anomaly': np.isin(x, anomaly_indices)
        })


class Header:
    """Верхняя панель приложения"""
    
    def __init__(self):
        with ui.header().classes('w-full bg-blue-600 text-white shadow-md p-4'):
            with ui.row().classes('w-full justify-between items-center'):
                ui.label('📊 ANALYTICS SYSTEM').classes('text-2xl font-bold')
                ui.label('v1.0.0').classes('text-sm opacity-75')


class Footer:
    """Нижняя панель приложения"""
    
    def __init__(self):
        with ui.footer().classes('w-full bg-gray-800 text-white text-center p-4'):
            ui.label('© 2024 Analytics System | Powered by Python + NiceGUI')


class DashboardTab:
    """Вкладка с общей статистикой и кластеризацией"""
    
    def __init__(self):
        self.df_clusters = DataGenerator.generate_clusters_data()
        self.render()
    
    def render(self):
        with ui.column().classes('w-full gap-4'):
            # Таблица статистики кластеров
            with ui.card().classes('w-full shadow-lg rounded-xl p-4'):
                ui.label('📋 Статистика кластеров').classes('text-lg font-bold mb-2')
                
                stats_df = pd.DataFrame({
                    'Кластер': ['Cluster 0', 'Cluster 1', 'Cluster 2'],
                    'Количество': [50, 50, 50],
                    'Mean (P1)': self.df_clusters.groupby('cluster')['param1'].mean().round(2).values,
                    'Std (P1)': self.df_clusters.groupby('cluster')['param1'].std().round(2).values,
                })
                
                columns = [
                    {'name': 'Кластер', 'label': 'Кластер', 'field': 'Кластер'},
                    {'name': 'Количество', 'label': 'Количество', 'field': 'Количество'},
                    {'name': 'Mean', 'label': 'Mean (P1)', 'field': 'Mean (P1)'},
                    {'name': 'Std', 'label': 'Std (P1)', 'field': 'Std (P1)'},
                ]
                ui.table(columns=columns, rows=stats_df.to_dict('records')).classes('w-full')
            
            # График распределения по кластерам
            fig_bar = go.Figure(data=[
                go.Bar(x=['Cluster 0', 'Cluster 1', 'Cluster 2'], 
                      y=[50, 50, 50],
                      marker_color=['#2563eb', '#16a34a', '#f59e0b'])
            ])
            fig_bar.update_layout(title='Распределение по кластерам', 
                                 height=400, margin=dict(l=0, r=0, t=30, b=0))
            ChartCard('📊 Bar Chart', fig_bar)
            
            # Круговая диаграмма
            fig_pie = go.Figure(data=[
                go.Pie(labels=['Cluster 0', 'Cluster 1', 'Cluster 2'], 
                      values=[50, 50, 50],
                      marker=dict(colors=['#2563eb', '#16a34a', '#f59e0b']))
            ])
            fig_pie.update_layout(title='Доля кластеров', height=400)
            ChartCard('🥧 Pie Chart', fig_pie)
            
            # Тренд средних значений
            fig_line = go.Figure()
            for i in range(3):
                cluster_data = self.df_clusters[self.df_clusters['cluster'] == i]
                fig_line.add_trace(go.Scatter(
                    y=cluster_data['param1'].values,
                    mode='lines',
                    name=f'Cluster {i}',
                    line=dict(width=2)
                ))
            fig_line.update_layout(title='Тренд параметров по кластерам', 
                                  height=400, margin=dict(l=0, r=0, t=30, b=0))
            ChartCard('📈 Line Trend', fig_line)


class TrendsTab:
    """Вкладка для временных рядов и прогнозов"""
    
    def __init__(self):
        self.df_ts = DataGenerator.generate_timeseries_data()
        self.render()
    
    def render(self):
        with ui.column().classes('w-full gap-4'):
            # Фильтры
            with ui.card().classes('w-full shadow-lg rounded-xl p-4'):
                ui.label('🔍 Фильтры').classes('text-lg font-bold mb-2')
                with ui.row().classes('gap-4 w-full'):
                    ui.label('Диапазон дат:').classes('self-center')
                    start_date = ui.date(value='2024-01-01')
                    ui.label('-').classes('self-center')
                    end_date = ui.date(value='2024-04-10')
                    ui.button('Применить').classes('bg-blue-600 text-white')
            
            # График с реальными и предсказанными значениями
            fig_forecast = go.Figure()
            fig_forecast.add_trace(go.Scatter(
                x=self.df_ts['date'],
                y=self.df_ts['actual'],
                mode='lines',
                name='Актуальные значения',
                line=dict(color='#2563eb', width=2)
            ))
            fig_forecast.add_trace(go.Scatter(
                x=self.df_ts['date'],
                y=self.df_ts['predicted'],
                mode='lines',
                name='Прогноз',
                line=dict(color='#16a34a', width=2, dash='dash')
            ))
            fig_forecast.update_layout(title='Прогноз vs Актуальные значения', 
                                      height=400, margin=dict(l=0, r=0, t=30, b=0),
                                      hovermode='x unified')
            ChartCard('📊 Forecast', fig_forecast)
            
            # График параметра
            fig_param = go.Figure()
            fig_param.add_trace(go.Scatter(
                x=self.df_ts['date'],
                y=self.df_ts['parameter'],
                mode='lines+markers',
                name='Параметр',
                line=dict(color='#f59e0b', width=2),
                marker=dict(size=4)
            ))
            fig_param.update_layout(title='Динамика параметра', 
                                   height=400, margin=dict(l=0, r=0, t=30, b=0))
            ChartCard('📈 Parameter Trend', fig_param)


class AnomaliesTab:
    """Вкладка для визуализации отклонений и аномалий"""
    
    def __init__(self):
        self.df_anom = DataGenerator.generate_anomalies_data()
        self.render()
    
    def render(self):
        with ui.column().classes('w-full gap-4'):
            # Scatter plot с выделением аномалий
            fig_scatter = go.Figure()
            
            normal = self.df_anom[~self.df_anom['is_anomaly']]
            anomalies = self.df_anom[self.df_anom['is_anomaly']]
            
            fig_scatter.add_trace(go.Scatter(
                x=normal['x'],
                y=normal['y'],
                mode='markers',
                name='Норма',
                marker=dict(color='#2563eb', size=6, opacity=0.7)
            ))
            fig_scatter.add_trace(go.Scatter(
                x=anomalies['x'],
                y=anomalies['y'],
                mode='markers',
                name='Аномалия',
                marker=dict(color='#ef4444', size=10, symbol='diamond', line=dict(width=2))
            ))
            fig_scatter.update_layout(title='Выявленные аномалии', 
                                     height=400, margin=dict(l=0, r=0, t=30, b=0))
            ChartCard('🔴 Anomalies Scatter', fig_scatter)
            
            # Гистограмма ошибок
            fig_hist = go.Figure()
            fig_hist.add_trace(go.Histogram(
                x=self.df_anom['error'],
                nbinsx=30,
                marker_color='#16a34a',
                name='Ошибки'
            ))
            fig_hist.update_layout(title='Распределение ошибок модели', 
                                  height=400, margin=dict(l=0, r=0, t=30, b=0))
            ChartCard('📊 Error Distribution', fig_hist)
            
            # Таблица последних аномалий
            with ui.card().classes('w-full shadow-lg rounded-xl p-4'):
                ui.label('⚠️ Последние выявленные аномалии').classes('text-lg font-bold mb-2')
                
                recent_anomalies = self.df_anom[self.df_anom['is_anomaly']].tail(10)
                anom_df = pd.DataFrame({
                    'ID': range(len(recent_anomalies)),
                    'X': recent_anomalies['x'].astype(int).values,
                    'Y': recent_anomalies['y'].round(2).values,
                    'Ошибка': recent_anomalies['error'].round(2).values,
                    'Статус': ['🔴 Anomaly'] * len(recent_anomalies)
                })
                
                columns = [
                    {'name': 'ID', 'label': 'ID', 'field': 'ID'},
                    {'name': 'X', 'label': 'X', 'field': 'X'},
                    {'name': 'Y', 'label': 'Y', 'field': 'Y'},
                    {'name': 'Ошибка', 'label': 'Ошибка', 'field': 'Ошибка'},
                    {'name': 'Статус', 'label': 'Статус', 'field': 'Статус'},
                ]
                ui.table(columns=columns, rows=anom_df.to_dict('records')).classes('w-full')


class MainTabs:
    """Главный блок с табами"""
    
    def __init__(self):
        with ui.tabs().classes('w-full justify-center mb-4') as tabs:
            ui.tab('Обзор')
            ui.tab('Тренды')
            ui.tab('Аномалии')
        
        with ui.tab_panels(tabs, value='Обзор').classes('w-full'):
            with ui.tab_panel('Обзор').classes('p-4 flex flex-col items-center gap-6'):
                DashboardTab()
            with ui.tab_panel('Тренды').classes('p-4 flex flex-col items-center gap-6'):
                TrendsTab()
            with ui.tab_panel('Аномалии').classes('p-4 flex flex-col items-center gap-6'):
                AnomaliesTab()


class AppLayout:
    """Общий контейнер интерфейса"""
    
    def __init__(self):
        # Хедер
        Header()
        
        # Основной контент
        with ui.column().classes('w-full max-w-7xl mx-auto px-4 py-6'):
            MainTabs()
        
        # Футер
        Footer()


def main():
    """Главная функция приложения"""
    ui.page_title('Analytics System')
    ui.query('body').style('background: #f8fafc;')
    
    AppLayout()


if __name__ in {"__main__", "__mp_main__"}:
    @ui.page("/")
    def index():
        main()
    ui.run(port=8080)