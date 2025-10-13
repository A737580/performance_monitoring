# app/core/data_generator.py
import os
import random
import pandas as pd
from datetime import datetime, timedelta

def generate_iot_error_data(
    days: int = 14,
    errors_per_day: tuple = (20, 50),
    output_dir: str = "app/data/raw"
):
    """Генерирует CSV файлы с ошибками станка для нескольких дней."""

    os.makedirs(output_dir, exist_ok=True)
    start_date = datetime.now() - timedelta(days=days)

    error_codes = ["E01", "E02", "E03", "E04", "E05"]
    # Параметр может отражать условную "интенсивность" ошибки
    parameter_ranges = {
        "E01": (10, 40),
        "E02": (5, 25),
        "E03": (20, 70),
        "E04": (15, 50),
        "E05": (30, 90),
    }

    all_days = []

    for d in range(days):
        current_date = start_date + timedelta(days=d)
        num_errors = random.randint(*errors_per_day)
        day_data = []

        for _ in range(num_errors):
            code = random.choice(error_codes)
            param = random.uniform(*parameter_ranges[code])
            day_data.append({
                "export_time": current_date.strftime("%Y-%m-%d"),
                "error_code": code,
                "parameter_value": round(param, 2),
            })

        df = pd.DataFrame(day_data)
        filename = os.path.join(output_dir, f"errors_{current_date.strftime('%Y_%m_%d')}.csv")
        df.to_csv(filename, index=False)
        all_days.append(df)

    print(f"✅ Generated {len(all_days)} CSV files in {output_dir}")
    return pd.concat(all_days, ignore_index=True)
