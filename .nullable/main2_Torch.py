import sys
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QHBoxLayout,
)
from PySide6.QtCore import Qt


# === 1. Простая нейросеть AutoEncoder ===
class AutoEncoder(nn.Module):
    def __init__(self, input_dim, latent_dim=2):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 8), nn.ReLU(), nn.Linear(8, latent_dim)
        )
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, 8), nn.ReLU(), nn.Linear(8, input_dim)
        )

    def forward(self, x):
        z = self.encoder(x)
        out = self.decoder(z)
        return out, z


# === 2. GUI-приложение ===
class ClusterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Autoencoder-анализ производительности")
        self.setMinimumSize(900, 600)

        # UI
        self.load_btn = QPushButton("Загрузить CSV")
        self.analyze_btn = QPushButton("Обучить и проанализировать")
        self.status_label = QLabel("Выберите файл для анализа")
        self.table = QTableWidget()

        # Макет
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.load_btn)
        top_layout.addWidget(self.analyze_btn)
        top_layout.addStretch()
        top_layout.addWidget(self.status_label)

        layout = QVBoxLayout()
        layout.addLayout(top_layout)
        layout.addWidget(self.table)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Действия
        self.load_btn.clicked.connect(self.load_file)
        self.analyze_btn.clicked.connect(self.analyze_data)

        # Данные
        self.df = None
        self.agg = None

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выбрать CSV", "", "CSV файлы (*.csv)"
        )
        if not file_path:
            return
        try:
            self.df = pd.read_csv(file_path)
            self.status_label.setText(f"Загружен файл: {file_path.split('/')[-1]}")
        except Exception as e:
            self.status_label.setText(f"Ошибка загрузки: {e}")

    def analyze_data(self):
        if self.df is None:
            self.status_label.setText("Сначала загрузите CSV!")
            return

        try:
            # === 1. Агрегация ===
            agg = (
                self.df.groupby(
                    ["export_time", "machine_id", "operator_id", "error_code"]
                )["value"]
                .agg(["count", "mean"])
                .reset_index()
                .pivot_table(
                    index=["export_time", "machine_id", "operator_id"],
                    columns="error_code",
                    values="count",
                    fill_value=0,
                )
                .reset_index()
            )

            # === 2. Препроцессинг ===
            X = agg.drop(columns=["export_time", "machine_id", "operator_id"])
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            X_tensor = torch.tensor(X_scaled, dtype=torch.float32)

            # === 3. Обучение AutoEncoder ===
            model = AutoEncoder(input_dim=X.shape[1])
            optimizer = optim.Adam(model.parameters(), lr=0.01)
            loss_fn = nn.MSELoss()

            for epoch in range(200):
                optimizer.zero_grad()
                out, _ = model(X_tensor)
                loss = loss_fn(out, X_tensor)
                loss.backward()
                optimizer.step()

            # === 4. Оценка аномальности ===
            with torch.no_grad():
                recon, Z = model(X_tensor)
                mse = torch.mean((recon - X_tensor) ** 2, dim=1).numpy()

            agg["recon_error"] = mse

            # === 5. Визуализация ===
            pca = PCA(n_components=2)
            Z_pca = pca.fit_transform(Z.numpy())
            plt.figure(figsize=(6, 5))
            scatter = plt.scatter(Z_pca[:, 0], Z_pca[:, 1], c=mse, cmap="plasma")
            plt.colorbar(scatter, label="Ошибка восстановления (аномальность)")
            plt.title("Анализ смен (AutoEncoder)")
            plt.xlabel("Latent 1")
            plt.ylabel("Latent 2")
            plt.show()

            # === 6. Таблица ===
            self.show_table(agg)
            self.status_label.setText(
                "Анализ завершён ✅ (чем выше ошибка, тем сильнее аномалия)"
            )

        except Exception as e:
            self.status_label.setText(f"Ошибка анализа: {e}")

    def show_table(self, df: pd.DataFrame):
        self.table.clear()
        self.table.setRowCount(len(df))
        self.table.setColumnCount(len(df.columns))
        self.table.setHorizontalHeaderLabels(df.columns.astype(str).tolist())

        for i, row in df.iterrows():
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setFlags(Qt.ItemIsEnabled)
                self.table.setItem(i, j, item)

        self.table.resizeColumnsToContents()


def main():
    app = QApplication(sys.argv)
    window = ClusterApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
