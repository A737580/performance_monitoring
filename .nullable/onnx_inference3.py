import onnxruntime as ort
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


# === 1. Загружаем ONNX модель ===
session = ort.InferenceSession("autoencoder_model.onnx")

# === 2. Загружаем новые данные ===
df = pd.read_csv("iot_errors_new.csv")  # новая выгрузка
agg = (
    df.groupby(["export_time", "machine_id", "operator_id", "error_code"])["value"]
    .agg(["count", "mean"])
    .reset_index()
    .pivot_table(
        index=["export_time", "machine_id", "operator_id"],
        columns="error_code",
        values="count",
        fill_value=0
    )
    .reset_index()
)
X = agg.drop(columns=["export_time", "machine_id", "operator_id"])
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X).astype(np.float32)

# === 3. Инференс ===
inputs = {"input": X_scaled}
outputs = session.run(["output", "latent"], inputs)
reconstructed = outputs[0]
latent = outputs[1]

# === 4. Подсчет ошибки восстановления ===
mse = np.mean((reconstructed - X_scaled) ** 2, axis=1)
agg["recon_error"] = mse

# === 5. Визуализация ===
pca = PCA(n_components=2)
Z_pca = pca.fit_transform(latent)
plt.scatter(Z_pca[:, 0], Z_pca[:, 1], c=mse, cmap="plasma")
plt.colorbar(label="Ошибка восстановления (аномальность)")
plt.title("ONNX-анализ производительности смен")
plt.show()

# === 6. Сохранение отчета ===
agg.to_csv("anomaly_report.csv", index=False)
print("✅ Анализ завершен. Результаты сохранены в anomaly_report.csv")
