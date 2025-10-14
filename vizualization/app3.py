from nicegui import ui, app
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List, Dict, Optional
import plotly.graph_objects as go
import plotly.express as px


# ==================== Data Models ====================

@dataclass
class Session:
    session_id: str
    date: str
    duration_min: float
    total_signals: int
    signals_per_minute: float
    discrete_ratio: float
    analog_ratio: float
    avg_discrete_active: float
    unique_discrete: int
    avg_analog_abs: float
    max_analog: float
    std_analog: float
    total_unique_signals: int
    rare_signal_ratio: float
    cluster: int


class DataGenerator:
    """Generate synthetic data for demonstration"""
    
    @staticmethod
    def generate_sessions(days: int = 30) -> List[Session]:
        sessions = []
        session_count = 0
        
        for day_offset in range(days):
            date = (datetime.now() - timedelta(days=days - day_offset)).strftime("%Y-%m-%d")
            daily_sessions = np.random.randint(3, 8)
            
            for _ in range(daily_sessions):
                session_count += 1
                cluster = np.random.choice([0, 1, 2], p=[0.6, 0.25, 0.15])
                
                if cluster == 0:  # Stable
                    duration = np.random.normal(45, 10)
                    signals = int(np.random.normal(150, 30))
                    max_analog = np.random.normal(15, 5)
            
                elif cluster == 1:  # Noisy
                    duration = np.random.normal(35, 8)
                    signals = int(np.random.normal(200, 40))
                    max_analog = np.random.normal(25, 8)
                else:  # Anomalous
                    duration = np.random.normal(20, 5)
                    signals = int(np.random.normal(100, 20))
                    max_analog = np.random.normal(80, 20)
                
                duration = max(5, duration)
                signals = max(10, signals)
                
                session = Session(
                    session_id=f"{date}_{session_count}",
                    date=date,
                    duration_min=duration,
                    total_signals=signals,
                    signals_per_minute=signals / duration,
                    discrete_ratio=np.random.uniform(0.3, 0.7),
                    analog_ratio=np.random.uniform(0.3, 0.7),
                    avg_discrete_active=np.random.uniform(0.2, 0.8),
                    unique_discrete=np.random.randint(5, 20),
                    avg_analog_abs=max_analog * np.random.uniform(0.5, 0.9),
                    max_analog=max_analog,
                    std_analog=max_analog * np.random.uniform(0.1, 0.4),
                    total_unique_signals=np.random.randint(15, 50),
                    rare_signal_ratio=np.random.uniform(0.05, 0.25),
                    cluster=cluster
                )
                sessions.append(session)
        
        return sessions


# ==================== UI Components ====================

class Header:
    """Top navigation and branding"""
    
    @staticmethod
    def create():
        with ui.header(elevated=True).classes('w-full bg-slate-800 text-white'):
            with ui.row().classes('w-full items-center justify-between px-6 py-4'):
                ui.label('Performance Analytics System').classes('text-2xl font-bold')
                with ui.row().classes('gap-4'):
                    ui.button(icon='search', flat=True, color='white')
                    ui.button(icon='person', flat=True, color='white')


class Footer:
    """Bottom information bar"""
    
    @staticmethod
    def create():
        with ui.footer(elevated=True).classes('w-full bg-slate-700 text-white'):
            with ui.row().classes('w-full items-center justify-between px-6 py-3'):
                ui.label('Cluster model v0.2 — Unsupervised analysis').classes('text-sm')
                ui.label(f'Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}').classes('text-sm text-gray-400')


class Chart:
    """Reusable chart component"""
    
    @staticmethod
    def scatter_plot(sessions: List[Session], title: str) -> go.Figure:
        df = pd.DataFrame([
            {
                'max_analog': s.max_analog,
                'signals_per_minute': s.signals_per_minute,
                'cluster': s.cluster,
                'duration': s.duration_min,
                'session': s.session_id
            }
            for s in sessions
        ])
        
        cluster_names = {0: 'Stable', 1: 'Noisy', 2: 'Anomalous'}
        cluster_colors = {0: '#3b82f6', 1: '#f59e0b', 2: '#ef4444'}
        
        fig = go.Figure()
        for cluster in [0, 1, 2]:
            cluster_data = df[df['cluster'] == cluster]
            fig.add_trace(go.Scatter(
                x=cluster_data['signals_per_minute'],
                y=cluster_data['max_analog'],
                mode='markers',
                name=cluster_names[cluster],
                marker=dict(size=cluster_data['duration'], color=cluster_colors[cluster], opacity=0.7),
                text=cluster_data['session'],
                hovertemplate='<b>%{text}</b><br>Signals/min: %{x:.2f}<br>Max Analog: %{y:.2f}<extra></extra>'
            ))
        
        fig.update_layout(
            title=title,
            xaxis_title='Signals per Minute',
            yaxis_title='Max Analog Value',
            height=400,
            template='plotly_white',
            showlegend=True
        )
        return fig

    @staticmethod
    def cluster_heatmap(sessions: List[Session]) -> go.Figure:
        df = pd.DataFrame([
            {
                'date': s.date,
                'cluster': s.cluster,
                'signals': s.total_signals
            }
            for s in sessions
        ])
        
        pivot = df.groupby(['date', 'cluster'])['signals'].count().reset_index()
        pivot_table = pivot.pivot(index='date', columns='cluster', values='signals').fillna(0)
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot_table.values,
            x=['Stable', 'Noisy', 'Anomalous'],
            y=pivot_table.index,
            colorscale='YlOrRd'
        ))
        
        fig.update_layout(title='Session Clusters Over Time', height=350, template='plotly_white')
        return fig

    @staticmethod
    def daily_stability_line(sessions: List[Session]) -> go.Figure:
        df = pd.DataFrame([
            {
                'date': s.date,
                'cluster': s.cluster
            }
            for s in sessions
        ])
        
        daily_stability = df.groupby('date').apply(
            lambda x: (x['cluster'] == 0).sum() / len(x) * 100
        ).reset_index()
        daily_stability.columns = ['date', 'stability_percent']
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=daily_stability['date'],
            y=daily_stability['stability_percent'],
            mode='lines+markers',
            name='Stability %',
            line=dict(color='#10b981', width=2),
            marker=dict(size=6)
        ))
        
        fig.update_layout(
            title='Daily Stability Trend',
            xaxis_title='Date',
            yaxis_title='Stable Sessions (%)',
            height=350,
            template='plotly_white'
        )
        return fig

    @staticmethod
    def monthly_summary(sessions: List[Session]) -> go.Figure:
        df = pd.DataFrame([
            {
                'date': s.date,
                'cluster': s.cluster,
                'signals_per_minute': s.signals_per_minute
            }
            for s in sessions
        ])
        
        df['month'] = pd.to_datetime(df['date']).dt.to_period('M').astype(str)
        
        monthly = df.groupby('month').agg({
            'cluster': lambda x: (x == 0).sum() / len(x) * 100,
            'signals_per_minute': 'mean'
        }).reset_index()
        monthly.columns = ['month', 'stability_percent', 'avg_signals_per_min']
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=monthly['month'],
            y=monthly['stability_percent'],
            name='Avg Stability %',
            marker_color='#8b5cf6'
        ))
        
        fig.update_layout(
            title='Monthly Performance Summary',
            xaxis_title='Month',
            yaxis_title='Avg Stability (%)',
            height=350,
            template='plotly_white'
        )
        return fig


class Layout:
    """Page layout structures"""
    
    @staticmethod
    def create_tab_content():
        pass


class AnalyticsDashboard:
    """Main application controller"""
    
    def __init__(self):
        self.sessions = DataGenerator.generate_sessions(days=30)
        self.selected_chart = None
    
    def build(self):
        Header.create()
        
        with ui.tabs().classes('w-full') as tabs:
            with ui.tab('Overview').classes('w-full'):
                self.build_overview_tab()
            
            with ui.tab('Cluster Analysis').classes('w-full'):
                self.build_cluster_tab()
            
            with ui.tab('Export').classes('w-full'):
                self.build_export_tab()
        
        Footer.create()
    
    def build_overview_tab(self):
        with ui.column().classes('w-full gap-6 p-6'):
            # Summary metrics
            with ui.row().classes('w-full gap-4'):
                with ui.card().classes('flex-1'):
                    ui.label('Total Sessions').classes('text-sm text-gray-600')
                    ui.label(str(len(self.sessions))).classes('text-3xl font-bold text-blue-600')
                
                with ui.card().classes('flex-1'):
                    stable_count = sum(1 for s in self.sessions if s.cluster == 0)
                    stability_pct = (stable_count / len(self.sessions)) * 100
                    ui.label('Stability Rate').classes('text-sm text-gray-600')
                    ui.label(f'{stability_pct:.1f}%').classes('text-3xl font-bold text-green-600')
                
                with ui.card().classes('flex-1'):
                    avg_signals = np.mean([s.signals_per_minute for s in self.sessions])
                    ui.label('Avg Signals/Min').classes('text-sm text-gray-600')
                    ui.label(f'{avg_signals:.1f}').classes('text-3xl font-bold text-orange-600')
            
            # Charts
            with ui.row().classes('w-full gap-4'):
                with ui.card().classes('flex-1'):
                    chart1 = Chart.scatter_plot(self.sessions, 'Session Performance Scatter')
                    ui.plotly(chart1).classes('w-full')
                
                with ui.card().classes('flex-1'):
                    chart2 = Chart.cluster_heatmap(self.sessions)
                    ui.plotly(chart2).classes('w-full')
            
            # Trends
            with ui.row().classes('w-full gap-4'):
                with ui.card().classes('flex-1'):
                    chart3 = Chart.daily_stability_line(self.sessions)
                    ui.plotly(chart3).classes('w-full')
                
                with ui.card().classes('flex-1'):
                    chart4 = Chart.monthly_summary(self.sessions)
                    ui.plotly(chart4).classes('w-full')
    
    def build_cluster_tab(self):
        with ui.column().classes('w-full gap-6 p-6'):
            ui.label('Cluster Characteristics').classes('text-xl font-bold')
            
            cluster_info = {
                0: {'name': 'Stable', 'color': 'bg-blue-100', 'description': 'Low signals/min, predictable behavior'},
                1: {'name': 'Noisy', 'color': 'bg-orange-100', 'description': 'High signals/min, many unique signals'},
                2: {'name': 'Anomalous', 'color': 'bg-red-100', 'description': 'Very high max_analog or short duration'}
            }
            
            with ui.row().classes('w-full gap-4'):
                for cluster_id, info in cluster_info.items():
                    count = sum(1 for s in self.sessions if s.cluster == cluster_id)
                    pct = (count / len(self.sessions)) * 100
                    
                    with ui.card().classes(f'flex-1 {info["color"]}'):
                        ui.label(info['name']).classes('text-lg font-bold')
                        ui.label(f'{count} sessions ({pct:.1f}%)').classes('text-sm text-gray-700')
                        ui.label(info['description']).classes('text-xs text-gray-600 mt-2')
            
            # Detailed comparison table
            ui.label('Cluster Metrics Comparison').classes('text-lg font-bold mt-6')
            
            with ui.row().classes('w-full overflow-x-auto'):
                cluster_data = []
                for cid in [0, 1, 2]:
                    cluster_sessions = [s for s in self.sessions if s.cluster == cid]
                    if cluster_sessions:
                        cluster_data.append({
                            'Cluster': cluster_info[cid]['name'],
                            'Avg Duration (min)': f"{np.mean([s.duration_min for s in cluster_sessions]):.1f}",
                            'Avg Signals/min': f"{np.mean([s.signals_per_minute for s in cluster_sessions]):.1f}",
                            'Max Analog (avg)': f"{np.mean([s.max_analog for s in cluster_sessions]):.1f}",
                            'Unique Signals (avg)': f"{np.mean([s.total_unique_signals for s in cluster_sessions]):.1f}"
                        })
                
                df_table = pd.DataFrame(cluster_data)
                ui.table(
                    columns=[{'name': col, 'label': col, 'field': col} for col in df_table.columns],
                    rows=df_table.to_dict('records'),
                    title='Cluster Metrics'
                ).classes('w-full')
    
    def build_export_tab(self):
        with ui.column().classes('w-full gap-6 p-6'):
            ui.label('Export & Configuration').classes('text-2xl font-bold')
            
            with ui.card().classes('w-full'):
                ui.label('Select Charts to Export').classes('text-lg font-bold')
                
                with ui.column().classes('gap-3'):
                    scatter_export = ui.checkbox('Session Performance Scatter', value=True)
                    heatmap_export = ui.checkbox('Cluster Heatmap', value=True)
                    stability_export = ui.checkbox('Daily Stability Trend', value=True)
                    monthly_export = ui.checkbox('Monthly Summary', value=True)
                    cluster_table_export = ui.checkbox('Cluster Metrics Table', value=True)
                
                ui.label('Export Format').classes('text-md font-bold mt-4')
                with ui.row().classes('gap-4'):
                    format_select = ui.select(
                        label='Format',
                        value='png',
                        options=['png', 'html', 'csv']
                    )
                
                ui.label('Export Options').classes('text-md font-bold mt-4')
                include_data = ui.checkbox('Include raw session data', value=False)
                include_stats = ui.checkbox('Include summary statistics', value=True)
                
                def on_export():
                    selected = {
                        'scatter': scatter_export.value,
                        'heatmap': heatmap_export.value,
                        'stability': stability_export.value,
                        'monthly': monthly_export.value,
                        'table': cluster_table_export.value
                    }
                    ui.notify(f'Export started: {format_select.value} format\nSelected charts: {sum(selected.values())}\nInclude data: {include_data.value}')
                
                ui.button('Export Selected', on_click=on_export, icon='download').classes('mt-4 bg-blue-600 text-white')


# ==================== Main Application ====================

if __name__ in {'__main__', '__mp_main__'}:
    dashboard = AnalyticsDashboard()
    dashboard.build()
    ui.run(host='0.0.0.0', port=8080)