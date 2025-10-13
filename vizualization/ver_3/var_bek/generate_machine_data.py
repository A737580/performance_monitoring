import pandas as pd
import random
from datetime import datetime, timedelta

# Параметры генерации
START_DATE = "2025-10-01"
NUM_DAYS = 5
UUID = "BA24F253-FC3C-4B89-A069-2768EFC1FA1B"
SIGNALS = ["A257", "A258", "A268", "A269", "A270", "A272", "A273", "A274", "A275"]

# Список для хранения строк
rows = []

event_counter = 1

# Генерация данных по дням
for day_offset in range(NUM_DAYS):
    current_date = datetime.strptime(START_DATE, "%Y-%m-%d") + timedelta(days=day_offset)
    
    # Сколько событий в этот день (от 3 до 8)
    num_events = random.randint(3, 8)
    
    for i in range(num_events):
        # Формат даты: DD.MM.YYYY HH:MM
        # Время — случайное в рабочие часы (8:00–17:00)
        hour = random.randint(8, 16)
        minute = random.randint(0, 59)
        event_time = current_date.replace(hour=hour, minute=minute).strftime("%d.%m.%Y %H:%M")
        
        signal = random.choice(SIGNALS)
        value_type = random.choice([11, 17])
        
        # Генерация значения в зависимости от типа
        if value_type == 11:
            val = random.choice([0, 1])
            text = str(val)
            big_int = str(val)
            double_val = ""
        else:  # value_type == 17
            val = round(random.uniform(-500, 500), 2)
            text = ""
            big_int = ""
            double_val = str(val)
        
        # Генерация ID вида "DD.xxx" (например, "01.abc")
        day_str = current_date.strftime("%d")
        suffix = "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=3))
        event_id = f"{day_str}.{suffix}"
        
        rows.append({
            "#": event_id,
            "UUID": UUID,
            "Signal": signal,
            "Event time": event_time,
            "Value type": str(value_type),
            "Text": text,
            "BigInt": big_int,
            "Timestamp": "",  # всегда пусто
            "Double": double_val
        })

# Создание DataFrame
df = pd.DataFrame(rows, columns=["#", "UUID", "Signal", "Event time", "Value type", "Text", "BigInt", "Timestamp", "Double"])

# Сохранение в файл с табуляцией
df.to_csv("machine_events.csv", sep="\t", index=False, na_rep="")

print("✅ Файл 'machine_events.csv' успешно сгенерирован!")
print(f"   Дней: {NUM_DAYS} | Событий: {len(df)}")