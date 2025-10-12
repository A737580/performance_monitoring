import pandas as pd
from sklearn.cluster import KMeans
from pathlib import Path

def analyze_clusters():
    raw_path = Path('app/data/raw')
    files = list(raw_path.glob('*.csv'))

    dfs = [pd.read_csv(f) for f in files]
    df = pd.concat(dfs, ignore_index=True)

    features = ['error_code', 'param_value']
    X = df[features]

    model = KMeans(n_clusters=3, random_state=42, n_init='auto')
    df['cluster'] = model.fit_predict(X)

    stats = df.groupby('cluster')['param_value'].agg(['count', 'mean', 'std']).reset_index()

    print("🔹 Кластеры сформированы:")
    print(stats)
    return df, stats
