# app/core/data_loader.py
import os
import pandas as pd

def load_all_error_data(directory: str = "app/data/raw") -> pd.DataFrame:
    """Собирает все CSV из указанной папки в единый DataFrame."""
    files = [f for f in os.listdir(directory) if f.endswith(".csv")]
    if not files:
        raise FileNotFoundError("❌ В директории нет CSV файлов.")

    dataframes = []
    for file in files:
        path = os.path.join(directory, file)
        df = pd.read_csv(path)
        dataframes.append(df)

    combined = pd.concat(dataframes, ignore_index=True)
    print(f"📦 Загружено {len(combined)} записей из {len(files)} файлов.")
    return combined
