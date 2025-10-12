import pandas as pd
import numpy as np
from pathlib import Path

def generate_csv_data(num_files=10, rows_per_file=50):
    raw_path = Path('app/data/raw')
    raw_path.mkdir(parents=True, exist_ok=True)

    for f in raw_path.glob('*.csv'):
        f.unlink()

    for i in range(num_files):
        data = {
            'error_code': np.random.randint(1, 6, size=rows_per_file),
            'param_value': np.random.normal(loc=30 + 10*i%3, scale=8, size=rows_per_file),
            'export_time': ['2025-01-01 18:00'] * rows_per_file,
        }
        pd.DataFrame(data).to_csv(raw_path / f'data_{i}.csv', index=False)

    print(f'✅ Generated {num_files} CSV files in {raw_path}')
