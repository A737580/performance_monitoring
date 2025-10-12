import sys
import pandas as pd
import numpy as np
import onnxruntime as ort
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QPushButton, QVBoxLayout, QWidget, QLabel, QTableWidget,
    QTableWidgetItem, QHBoxLayout
)
from PySide6.QtCore import Qt


class ONNXAnalyzerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI-анализ производительности (ONNX)")
        self.setMinimumSize(900, 600)

        # === UI элементы ===
        self.load_btn = QPushButton("Загрузить CSV")
        self.analyze_btn = QPushButton("Проанализировать (ONNX)")
        self.status_label = QLabel("Выберите файл для анализа")
        self.table = QTableWidget()

        layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.load_btn)
        top_layout.addWidget(self.analyze_btn)
        top_layout.addWidget(self.status_label)
        layout.addLayout(top_layout)
        layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # === Логика ===
        self.load_btn.clicked.connect(self.load_csv)
        self.analyze_btn.clicked.connect(self.analyze_csv)

        self.df = None
        self.model_path = "autoencoder_model.onnx"

        # Загружаем модель
        try:
            self.session = ort.InferenceSession(self.model_path)
            self.status_label.setText("✅ Модель ONNX загружена")
        except Exception as e:
            self.session = None
            self.status_label.setText(f"❌ Ошибка загрузки модели: {e}")

    def load_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выбрать CSV", "", "CSV файлы (*.csv)")
        if not file_path:
            return
        try:
            self.df = pd.read_csv(file_path)
            self.status_label.setText(f"Загружен файл: {file_path.split('/')[-1]}")
        except Exception as e:
            self.status_label.setText(f"Ошибка чтения файла: {e}")

    def analyze_csv(self):
        if self.df is None:
            self.status_label.setText("⚠️ Сначала загрузите CSV!")
            return
        if self.session is None:
            self.status_label.setText("❌ Нет загруженной модели ONNX!")
            return

        try:
            # === 1. Подготовка данных ===
            agg = (
                self.df.groupby(["export_time", "machine_id", "operator_id", "error_code"])["value"]
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

            # === 2. Инференс через ONNX ===
            inputs = {"input": X_scaled}
            outputs = self.session.run(["output", "latent"], inputs)
            reconstructed, latent = outputs

            # === 3. Расчет ошибки восстановления ===
            mse = np.mean((reconstructed - X_scaled) ** 2, axis=1)
            agg["recon_error"] = mse

            # === 4. Визуализация ===
            pca = PCA(n_components=2)
            Z_pca = pca.fit_transform(latent)
            plt.figure(figsize=(6, 5))
            scatter = plt.scatter(Z_pca[:, 0], Z_pca[:, 1], c=mse, cmap="plasma")
            plt.colorbar(scatter, label="Ошибка восстановления (аномальность)")
            plt.title("ONNX-анализ производительности смен")
            plt.xlabel("Latent 1")
            plt.ylabel("Latent 2")
            plt.show()

            # === 5. Таблица ===
            self.show_table(agg)
            self.status_label.setText("✅ Анализ завершен — чем выше ошибка, тем сильнее аномалия")

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
    window = ONNXAnalyzerApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
