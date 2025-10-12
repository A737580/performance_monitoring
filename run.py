# run.py
from app.core.data_generator import generate_iot_error_data
from app.core.data_loader import load_all_error_data
from app.core.clustering import clusterize_errors

if __name__ == "__main__":
    # 1️⃣ Генерация данных
    generate_iot_error_data(days=10)

    # 2️⃣ Загрузка данных
    df = load_all_error_data()

    # 3️⃣ Кластеризация
    df_clustered, stats, model = clusterize_errors(df, n_clusters=3)

    print("\nПример данных после кластеризации:")
    print(df_clustered.head())
