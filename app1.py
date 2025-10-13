import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from nicegui import ui
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


class ChartCard:
    """Универсальный класс для отображения графика с подписью и легендой"""
    
    def __init__(self, title: str, description: str, figure):
        with ui.card().classes('w-full shadow-lg rounded-xl p-4 bg-white'):
            ui.label(title).classes('text-lg font-bold mb-1 text-blue-600')
            ui.label(description).classes('text-sm text-gray-600 mb-3 italic')
            ui.plotly(figure).classes('w-full')


class DataGenerator:
    """Генератор тестовых данных"""
    
    @staticmethod
    def generate_error_data():
        """Генерирует данные о ошибках"""
        np.random.seed(42)
        dates = pd.date_range('2025-10-01', periods=30, freq='D')
        error_codes = ['E01', 'E02', 'E03', 'E04', 'E05']
        
        data = []
        for date in dates:
            for i, code in enumerate(error_codes):
                data.append({
                    'Дата выгрузки': date,
                    'Код ошибки': code,
                    'Значение параметра': np.random.uniform(0.1, 1.0),
                    'Кол-во повторов': np.random.randint(1, 50)
                })
        
        return pd.DataFrame(data)


class ScatterPlotChart:
    """Scatter Plot - каждая точка - ошибка, размер - кол-во повторов"""
    
    def __init__(self):
        df = DataGenerator.generate_error_data()
        
        fig = go.Figure()
        
        for code in df['Код ошибки'].unique():
            code_data = df[df['Код ошибки'] == code]
            fig.add_trace(go.Scatter(
                x=code_data['Дата выгрузки'],
                y=code_data['Значение параметра'],
                mode='markers',
                name=code,
                marker=dict(
                    size=code_data['Кол-во повторов'] / 5,
                    opacity=0.7,
                    line=dict(width=2)
                ),
                text=[f"Ошибка: {c}<br>Значение: {v:.2f}<br>Повторов: {r}" 
                      for c, v, r in zip(code_data['Код ошибки'], 
                                        code_data['Значение параметра'],
                                        code_data['Кол-во повторов'])],
                hovertemplate='%{text}<extra></extra>'
            ))
        
        fig.update_layout(
            title='Scatter Plot: Ошибки по параметрам и датам',
            xaxis_title='Дата выгрузки',
            yaxis_title='Значение параметра',
            height=500,
            hovermode='closest',
            template='plotly_white'
        )
        
        ChartCard('📍 Scatter Plot', 'Каждая точка - ошибка, размер - количество повторов', fig)


class BarChartByError:
    """Bar Chart - распределение ошибок по кодам"""
    
    def __init__(self):
        df = DataGenerator.generate_error_data()
        
        error_stats = df.groupby('Код ошибки').agg({
            'Кол-во повторов': 'sum',
            'Значение параметра': 'mean'
        }).reset_index()
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=error_stats['Код ошибки'],
            y=error_stats['Кол-во повторов'],
            marker_color='#2563eb',
            text=error_stats['Кол-во повторов'],
            textposition='auto',
            name='Всего повторов'
        ))
        
        fig.update_layout(
            title='Bar Chart: Статистика ошибок по кодам',
            xaxis_title='Код ошибки',
            yaxis_title='Кол-во повторов',
            height=400,
            template='plotly_white'
        )
        
        ChartCard('📊 Bar Chart', 'Распределение количества повторов по кодам ошибок', fig)


class BarChartByDate:
    """Bar Chart - распределение ошибок по датам"""
    
    def __init__(self):
        df = DataGenerator.generate_error_data()
        df['Дата'] = df['Дата выгрузки'].dt.strftime('%Y-%m-%d')
        
        date_stats = df.groupby('Дата')['Кол-во повторов'].sum().reset_index()
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=date_stats['Дата'],
            y=date_stats['Кол-во повторов'],
            marker_color='#16a34a',
            text=date_stats['Кол-во повторов'],
            textposition='auto',
            name='Повторы'
        ))
        
        fig.update_layout(
            title='Bar Chart: Динамика ошибок по дням',
            xaxis_title='Дата',
            yaxis_title='Кол-во повторов',
            height=400,
            template='plotly_white',
            xaxis={'tickangle': -45}
        )
        
        ChartCard('📈 Bar Chart by Date', 'Количество ошибок, зафиксированных в каждый день', fig)


class PieChart:
    """Pie Chart - доля каждого кода ошибки"""
    
    def __init__(self):
        df = DataGenerator.generate_error_data()
        
        error_dist = df.groupby('Код ошибки')['Кол-во повторов'].sum().reset_index()
        
        colors = ['#2563eb', '#16a34a', '#f59e0b', '#ef4444', '#8b5cf6']
        
        fig = go.Figure(data=[
            go.Pie(
                labels=error_dist['Код ошибки'],
                values=error_dist['Кол-во повторов'],
                marker=dict(colors=colors),
                textinfo='label+percent',
                hovertemplate='<b>%{label}</b><br>Повторов: %{value}<br>Доля: %{percent}<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title='Pie Chart: Распределение ошибок по типам',
            height=500,
            template='plotly_white'
        )
        
        ChartCard('🥧 Pie Chart', 'Процентное распределение типов ошибок', fig)


class LineChart:
    """Line Chart - тренд параметра во времени"""
    
    def __init__(self):
        df = DataGenerator.generate_error_data()
        
        daily_avg = df.groupby('Дата выгрузки')['Значение параметра'].mean().reset_index()
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=daily_avg['Дата выгрузки'],
            y=daily_avg['Значение параметра'],
            mode='lines+markers',
            name='Среднее значение',
            line=dict(color='#2563eb', width=3),
            marker=dict(size=6),
            fill='tozeroy',
            fillcolor='rgba(37, 99, 235, 0.2)'
        ))
        
        fig.update_layout(
            title='Line Chart: Тренд среднего значения параметра',
            xaxis_title='Дата',
            yaxis_title='Значение параметра',
            height=400,
            template='plotly_white',
            hovermode='x unified'
        )
        
        ChartCard('📉 Line Chart', 'Динамика среднего значения параметра ошибок', fig)


class HeatmapChart:
    """Heatmap - матрица: ошибки vs значения параметров"""
    
    def __init__(self):
        df = DataGenerator.generate_error_data()
        
        # Создаём матрицу ошибка x дата
        heatmap_data = df.pivot_table(
            index='Код ошибки',
            columns='Дата выгрузки',
            values='Кол-во повторов',
            fill_value=0
        )
        
        # Берём только последние 15 дней для наглядности
        heatmap_data = heatmap_data.iloc[:, -15:]
        
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data.values,
            x=heatmap_data.columns.strftime('%Y-%m-%d'),
            y=heatmap_data.index,
            colorscale='YlOrRd',
            hovertemplate='Ошибка: %{y}<br>Дата: %{x}<br>Повторов: %{z}<extra></extra>'
        ))
        
        fig.update_layout(
            title='Heatmap: Матрица ошибок по датам',
            xaxis_title='Дата',
            yaxis_title='Код ошибки',
            height=400,
            template='plotly_white',
            xaxis={'tickangle': -45}
        )
        
        ChartCard('🔥 Heatmap', 'Интенсивность ошибок по кодам и датам (тепловая карта)', fig)


class BoxPlotChart:
    """Box Plot - распределение параметров по ошибкам"""
    
    def __init__(self):
        df = DataGenerator.generate_error_data()
        
        fig = go.Figure()
        
        for code in sorted(df['Код ошибки'].unique()):
            code_data = df[df['Код ошибки'] == code]
            fig.add_trace(go.Box(
                y=code_data['Значение параметра'],
                name=code,
                boxmean='sd'
            ))
        
        fig.update_layout(
            title='Box Plot: Распределение значений параметров по кодам ошибок',
            yaxis_title='Значение параметра',
            height=400,
            template='plotly_white'
        )
        
        ChartCard('📦 Box Plot', 'Статистическое распределение параметров для каждой ошибки', fig)


class HistogramChart:
    """Histogram - распределение значений параметров"""
    
    def __init__(self):
        df = DataGenerator.generate_error_data()
        
        fig = go.Figure()
        
        for code in sorted(df['Код ошибки'].unique()):
            code_data = df[df['Код ошибки'] == code]
            fig.add_trace(go.Histogram(
                x=code_data['Значение параметра'],
                name=code,
                opacity=0.6,
                nbinsx=15
            ))
        
        fig.update_layout(
            title='Histogram: Распределение значений параметров',
            xaxis_title='Значение параметра',
            yaxis_title='Частота',
            barmode='overlay',
            height=400,
            template='plotly_white'
        )
        
        ChartCard('📊 Histogram', 'Частота значений параметров по разным кодам ошибок', fig)


class ClusterScatterPlot:
    """Scatter Plot с кластеризацией K-means"""
    
    def __init__(self):
        df = DataGenerator.generate_error_data()
        
        # Подготовка данных для кластеризации
        X = df[['Значение параметра', 'Кол-во повторов']].values
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # K-means кластеризация
        kmeans = KMeans(n_clusters=3, random_state=42)
        df['Cluster'] = kmeans.fit_predict(X_scaled)
        
        fig = go.Figure()
        
        colors = ['#2563eb', '#16a34a', '#f59e0b']
        for i in range(3):
            cluster_data = df[df['Cluster'] == i]
            fig.add_trace(go.Scatter(
                x=cluster_data['Значение параметра'],
                y=cluster_data['Кол-во повторов'],
                mode='markers',
                name=f'Cluster {i}',
                marker=dict(size=10, color=colors[i], opacity=0.7, line=dict(width=2)),
                text=[f"Ошибка: {c}<br>Значение: {v:.2f}<br>Повторов: {r}<br>Кластер: {cl}" 
                      for c, v, r, cl in zip(cluster_data['Код ошибки'],
                                            cluster_data['Значение параметра'],
                                            cluster_data['Кол-во повторов'],
                                            cluster_data['Cluster'])],
                hovertemplate='%{text}<extra></extra>'
            ))
        
        # Добавляем центроиды
        centers = scaler.inverse_transform(kmeans.cluster_centers_)
        fig.add_trace(go.Scatter(
            x=centers[:, 0],
            y=centers[:, 1],
            mode='markers',
            name='Центроиды',
            marker=dict(size=20, color='red', symbol='star', line=dict(width=2, color='darkred')),
            hovertemplate='Центроид<br>Значение: %{x:.2f}<br>Повторов: %{y:.0f}<extra></extra>'
        ))
        
        fig.update_layout(
            title='K-Means Clustering: Группировка ошибок по параметрам',
            xaxis_title='Значение параметра',
            yaxis_title='Кол-во повторов',
            height=500,
            template='plotly_white',
            hovermode='closest'
        )
        
        ChartCard('🎯 K-Means Clustering', 'Автоматическая группировка ошибок на 3 кластера', fig)


class BubbleChart:
    """Bubble Chart - 3D представление: дата, параметр, кол-во повторов"""
    
    def __init__(self):
        df = DataGenerator.generate_error_data()
        
        daily_error = df.groupby(['Дата выгрузки', 'Код ошибки']).agg({
            'Значение параметра': 'mean',
            'Кол-во повторов': 'sum'
        }).reset_index()
        
        fig = go.Figure()
        
        for code in sorted(daily_error['Код ошибки'].unique()):
            code_data = daily_error[daily_error['Код ошибки'] == code]
            fig.add_trace(go.Scatter(
                x=code_data['Дата выгрузки'],
                y=code_data['Значение параметра'],
                mode='markers',
                name=code,
                marker=dict(
                    size=code_data['Кол-во повторов'] / 3,
                    opacity=0.6,
                    line=dict(width=2)
                ),
                text=[f"Ошибка: {c}<br>Дата: {d.strftime('%Y-%m-%d')}<br>Значение: {v:.2f}<br>Повторов: {r}" 
                      for c, d, v, r in zip(code_data['Код ошибки'],
                                           code_data['Дата выгрузки'],
                                           code_data['Значение параметра'],
                                           code_data['Кол-во повторов'])],
                hovertemplate='%{text}<extra></extra>'
            ))
        
        fig.update_layout(
            title='Bubble Chart: Ошибки во времени (размер = повторы)',
            xaxis_title='Дата',
            yaxis_title='Значение параметра',
            height=500,
            template='plotly_white',
            hovermode='closest'
        )
        
        ChartCard('🫧 Bubble Chart', 'Трёхмерное представление: дата, параметр, количество повторов', fig)


class Header:
    """Верхняя панель"""
    
    def __init__(self):
        with ui.header().classes('w-full bg-gradient-to-r from-blue-600 to-blue-800 text-white shadow-md p-4'):
            with ui.row().classes('w-full justify-between items-center'):
                ui.label('📊 CHART TYPES SHOWCASE').classes('text-2xl font-bold')
                ui.label('K-Means Clustering & Error Analysis').classes('text-sm opacity-75')


class Footer:
    """Нижняя панель"""
    
    def __init__(self):
        with ui.footer().classes('w-full bg-gray-900 text-white text-center p-4'):
            ui.label('© 2025 Analytics | Все типы графиков для анализа ошибок и кластеризации')


def main():
    """Главная функция"""
    ui.page_title('Chart Types Showcase')
    ui.query('body').style('background: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%);')
    
    Header()
    
    with ui.column().classes('w-full max-w-7xl mx-auto px-4 py-6 gap-6'):
        ui.label('Все типы графиков для анализа данных об ошибках').classes('text-3xl font-bold text-center text-blue-700 mb-4')
        ui.label('Выберите вкладку для просмотра различных визуализаций данных').classes('text-center text-gray-600 mb-6')
        
        with ui.tabs().classes('w-full'):
            with ui.tab('📍 Scatter & Bubble'):
                with ui.column().classes('w-full gap-6'):
                    ScatterPlotChart()
                    BubbleChart()
            
            with ui.tab('📊 Bar & Pie'):
                with ui.column().classes('w-full gap-6'):
                    BarChartByError()
                    BarChartByDate()
                    PieChart()
            
            with ui.tab('📈 Line & Trends'):
                with ui.column().classes('w-full gap-6'):
                    LineChart()
                    BoxPlotChart()
            
            with ui.tab('🔥 Heatmap & Distribution'):
                with ui.column().classes('w-full gap-6'):
                    HeatmapChart()
                    HistogramChart()
            
            with ui.tab('🎯 Clustering'):
                with ui.column().classes('w-full gap-6'):
                    ClusterScatterPlot()
    
    Footer()


if __name__ in {"__main__", "__mp_main__"}:
    @ui.page("/")
    def index():
        main()
    ui.run(port=8080)