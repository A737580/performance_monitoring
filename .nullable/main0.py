import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# === 1. Синтетика выгрузок ошибок ===
np.random.seed(42)

machines = ["M001", "M002", "M003"]
operators = ["OP12", "OP09", "OP07"]
error_codes = ["E101", "E102", "E103", "E104"]

rows = []
for day in range(1, 11):  # 10 дней
    export_time = f"2025-10-{day:02d} 18:00:00"
    for m in machines:
        for op in operators:
            n_errors = np.random.randint(10, 50)
            for _ in range(n_errors):
                rows.append({
                    "export_time": export_time,
                    "machine_id": m,
                    "operator_id": op,
                    "error_code": np.random.choice(error_codes),
                    "value": abs(np.random.normal(2, 1))
                })

df = pd.DataFrame(rows)

# === 2. Агрегирование по дню/оператору/станку ===
agg = (
    df.groupby(["export_time", "machine_id", "operator_id", "error_code"])["value"]
    .agg(["count", "mean", "std"])
    .reset_index()
    .pivot_table(index=["export_time", "machine_id", "operator_id"],
                 columns="error_code",
                 values="count",
                 fill_value=0)
    .reset_index()
)

# === 3. Кластеризация профилей ошибок ===
X = agg.drop(columns=["export_time", "machine_id", "operator_id"])
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

kmeans = KMeans(n_clusters=3, random_state=42)
agg["cluster"] = kmeans.fit_predict(X_scaled)

# === 4. Визуализация ===
pca = PCA(n_components=2)
pca_result = pca.fit_transform(X_scaled)
agg["PC1"], agg["PC2"] = pca_result[:, 0], pca_result[:, 1]

plt.figure(figsize=(6,5))
plt.scatter(agg["PC1"], agg["PC2"], c=agg["cluster"], cmap="tab10")
plt.title("Кластеры дней по структуре ошибок")
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.show()

# === 5. Пример анализа ===
print(agg.head())
