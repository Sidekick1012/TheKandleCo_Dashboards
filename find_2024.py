import pandas as pd

df = pd.read_excel('The Kandle Co. Notes Working 2024-2025.xlsx', sheet_name='Notes', header=None)

for idx, row in df.iterrows():
    for col in range(len(row)):
        val = str(row[col])
        if '2024' in val:
            print(f"Row {idx} (Col {col}): {val.strip()}")
