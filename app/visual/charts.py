# app/visual/charts.py
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def ensure_export_time_date(df: pd.DataFrame) -> pd.DataFrame:
    """Убедиться, что в df есть колонка export_time в виде даты (pd.Timestamp.date)."""
    if 'export_time' not in df.columns:
        # если нет — создать фиктивную колонку
        df = df.copy()
        df['export_time'] = pd.to_datetime('2025-01-01')
        return df
    # пытаемся привести
    try:
        df = df.copy()
        df['export_time'] = pd.to_datetime(df['export_time']).dt.date
    except Exception:
        df['export_time'] = pd.to_datetime(df['export_time'], errors='coerce').dt.date
    return df

def fig_errors_by_day(df: pd.DataFrame, days: int = None):
    df2 = ensure_export_time_date(df)
    agg = df2.groupby('export_time').size().reset_index(name='count')
    if days:
        agg = agg.sort_values('export_time').tail(days)
    fig = px.bar(agg, x='export_time', y='count', title='Ошибки по дням', labels={'export_time':'Дата','count':'Кол-во ошибок'})
    fig.update_layout(margin=dict(l=10,r=10,t=40,b=10), height=360)
    return fig

def fig_error_code_distribution(df: pd.DataFrame, top_n: int = 10):
    if 'error_code' not in df.columns:
        # ничего не строим
        fig = go.Figure()
        fig.update_layout(title='Нет данных по кодам ошибок')
        return fig
    agg = df['error_code'].value_counts().reset_index()
    agg.columns = ['error_code', 'count']
    agg = agg.head(top_n)
    fig = px.bar(agg, x='error_code', y='count', title=f'Top {top_n} коды ошибок', labels={'error_code':'Код ошибки','count':'Частота'})
    fig.update_layout(margin=dict(l=10,r=10,t=40,b=10), height=360)
    return fig

def fig_parameter_histogram(df: pd.DataFrame, bins: int = 30):
    if 'parameter_value' not in df.columns:
        fig = go.Figure()
        fig.update_layout(title='Нет числового параметра для построения гистограммы')
        return fig
    fig = px.histogram(df, x='parameter_value', nbins=bins, title='Распределение параметра ошибок', labels={'parameter_value':'Значение параметра','count':'Частота'})
    fig.update_layout(margin=dict(l=10,r=10,t=40,b=10), height=320)
    return fig

def fig_scatter_clusters(df: pd.DataFrame):
    # выберем оси: parameter_value и порядковая дата (или export_time)
    df2 = df.copy()
    if 'parameter_value' not in df2.columns:
        df2['parameter_value'] = 0
    # create an index for vertical placement if export_time absent
    if 'export_time' in df2.columns:
        try:
            df2['_x'] = pd.to_datetime(df2['export_time'])
        except Exception:
            df2['_x'] = pd.RangeIndex(len(df2))
    else:
        df2['_x'] = pd.RangeIndex(len(df2))
    # cluster column
    color_col = 'cluster' if 'cluster' in df2.columns else None
    title = 'Кластеры ошибок — parameter vs day'
    fig = px.scatter(df2, x='_x', y='parameter_value', color=color_col, hover_data=['error_code'], title=title)
    fig.update_layout(margin=dict(l=10,r=10,t=40,b=10), height=420)
    return fig

def fig_box_by_cluster(df: pd.DataFrame):
    if 'cluster' not in df.columns:
        fig = go.Figure()
        fig.update_layout(title='Кластеры не найдены')
        return fig
    if 'parameter_value' not in df.columns:
        df['parameter_value'] = 0
    fig = px.box(df, x='cluster', y='parameter_value', color='cluster', points="all", title='Распределение параметра по кластерам')
    fig.update_layout(margin=dict(l=10,r=10,t=40,b=10), height=360)
    return fig
