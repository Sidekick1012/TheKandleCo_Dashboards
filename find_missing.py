import pandas as pd

df = pd.read_excel('The Kandle Co. Notes Working 2024-2025.xlsx', sheet_name='Notes', header=None)
months = ['SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER']

for idx, row in df.iloc[118:731].iterrows():
    for col in range(len(row)):
        val = str(row[col]).upper()
        for m in months:
            if m in val:
                print(f"Row {idx} (Col {col}): {val}")
