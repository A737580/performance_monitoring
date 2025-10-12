# app/core/clustering.py
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def clusterize_errors(df: pd.DataFrame, n_clusters: int = 3):
    """Простая кластеризация ошибок по параметру value."""
    # Код ошибки можно закодировать численно
    df_encoded = pd.get_dummies(df, columns=["error_code"])

    X = df_encoded[["parameter_value"] + [c for c in df_encoded.columns if "error_code_" in c]]
    X_scaled = StandardScaler().fit_transform(X)

    model = KMeans(n_clusters=n_clusters, random_state=42)
    df["cluster"] = model.fit_predict(X_scaled)

    cluster_stats = df.groupby("cluster")["parameter_value"].agg(["count", "mean", "std"]).reset_index()

    print("🔹 Кластеры сформированы:")
    print(cluster_stats)
    return df, cluster_stats, model
