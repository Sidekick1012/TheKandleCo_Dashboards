import pandas as pd

excel_file = "The Kandle Co. Notes Working 2024-2025.xlsx"

print(f"\n📊 Checking Excel file: {excel_file}\n")

try:
    excel_sheets = pd.read_excel(excel_file, sheet_name=None)
    
    print(f"Total Sheets: {len(excel_sheets)}\n")
    print("Sheet Names:")
    for i, sheet_name in enumerate(excel_sheets.keys(), 1):
        rows = len(excel_sheets[sheet_name])
        print(f"  {i}. {sheet_name} ({rows} rows)")
    
    print("\n" + "="*60)
    print("Summary:")
    total_rows = sum(len(df) for df in excel_sheets.values())
    print(f"Total rows across all sheets: {total_rows}")
    print("="*60 + "\n")
    
except Exception as e:
    print(f"Error: {e}")
