import pandas as pd
import numpy as np

# Загрузка данных (замените путь на свой)
# df = pd.read_csv("machine_events.csv", sep="\t")
# Пока используем пример

df = pd.read_csv('machine_events.csv', sep='\t')

# === Шаг 1: извлечь дату (без времени) ===
df["Date"] = pd.to_datetime(df["Event time"], format="%d.%m.%Y %H:%M").dt.date

# === Шаг 2: извлечь числовое значение ===
def get_value(row):
    if row["Value type"] == 11:
        return float(row["Text"]) if row["Text"] not in ("", None) else 0.0
    elif row["Value type"] == 17:
        return float(row["Double"]) if row["Double"] not in ("", None) else 0.0
    else:
        return 0.0

df["Value"] = df.apply(get_value, axis=1)

# === Шаг 3: определить полный список сигналов ===
ALL_SIGNALS = sorted(df["Signal"].unique())  # или задать вручную

# === Шаг 4: агрегация по дню ===
records = []

for date, group in df.groupby("Date"):
    rec = {"Date": date}
    
    # Считаем частоту и среднее значение по каждому сигналу
    signal_counts = group["Signal"].value_counts()
    signal_means = group.groupby("Signal")["Value"].mean()
    
    for sig in ALL_SIGNALS:
        rec[f"{sig}_count"] = int(signal_counts.get(sig, 0))
        rec[f"{sig}_mean_value"] = float(signal_means.get(sig, 0.0))
    
    # Общие признаки дня
    rec["total_signals"] = len(group)
    rec["unique_signals"] = group["Signal"].nunique()
    rec["avg_value"] = group["Value"].mean()
    rec["max_value"] = group["Value"].max()
    rec["min_value"] = group["Value"].min()
    rec["std_value"] = float(group["Value"].std()) if len(group) > 1 else 0.0
    rec["discrete_ratio"] = (group["Value type"] == 11).mean()
    rec["analog_ratio"] = (group["Value type"] == 17).mean()
    rec["rare_signal_ratio"] = (signal_counts == 1).sum() / len(signal_counts) if len(signal_counts) > 0 else 0.0
    
    records.append(rec)

# Создаём финальный датафрейм
df_daily = pd.DataFrame(records)

# Сортируем по дате
df_daily = df_daily.sort_values("Date").reset_index(drop=True)

# Сохраняем
df_daily.to_csv("daily_features.csv", index=False)

print("✅ Агрегированные дневные признаки сохранены в 'daily_features.csv'")
print("\nПример результата:")
print(df_daily.head())