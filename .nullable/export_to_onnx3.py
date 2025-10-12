import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
from sklearn.preprocessing import StandardScaler

class AutoEncoder(nn.Module):
    def __init__(self, input_dim, latent_dim=2):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 8), nn.ReLU(),
            nn.Linear(8, latent_dim)
        )
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, 8), nn.ReLU(),
            nn.Linear(8, input_dim)
        )

    def forward(self, x):
        z = self.encoder(x)
        out = self.decoder(z)
        return out, z


if __name__ == "__main__":
    # === 1. Загружаем данные ===
    df = pd.read_csv("iot_errors.csv")  # пример
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
    X_scaled = scaler.fit_transform(X)

    X_tensor = torch.tensor(X_scaled, dtype=torch.float32)

    # === 2. Обучаем AutoEncoder ===
    model = AutoEncoder(input_dim=X.shape[1])
    optimizer = optim.Adam(model.parameters(), lr=0.01)
    loss_fn = nn.MSELoss()

    for epoch in range(200):
        optimizer.zero_grad()
        out, _ = model(X_tensor)
        loss = loss_fn(out, X_tensor)
        loss.backward()
        optimizer.step()

    print("✅ Обучение завершено, экспортируем в ONNX...")

    # === 3. Экспорт ===
    dummy_input = torch.randn(1, X.shape[1])
    torch.onnx.export(
        model,
        dummy_input,
        "autoencoder_model.onnx",
        input_names=["input"],
        output_names=["output", "latent"],
        dynamic_axes={"input": {0: "batch_size"}, "output": {0: "batch_size"}},
        opset_version=17
    )

    print("💾 Модель сохранена как autoencoder_model.onnx")
