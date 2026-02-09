import pandas as pd
import re

df = pd.read_excel('The Kandle Co. Notes Working 2024-2025.xlsx', sheet_name='Notes', header=None)
pattern = r'([A-Za-z]+-\d{4})'

months_found = []
for idx, row in df.iterrows():
    for col in range(len(row)):
        val = str(row[col])
        match = re.search(pattern, val)
        if match:
            months_found.append((idx, col, match.group(1)))
            break

for idx, col, m in months_found:
    print(f"Row {idx} (Col {col}): {m}")
