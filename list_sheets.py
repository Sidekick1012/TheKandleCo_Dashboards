import pandas as pd

EXCEL_FILE = r"c:\Users\aqibr\OneDrive\Desktop\The_Kandle_c0_Dashboard\The Kandle Co. Notes Working 2024-2025.xlsx"

try:
    xls = pd.ExcelFile(EXCEL_FILE)
    print("Available Sheets:")
    for s in xls.sheet_names:
        print(f"- {s}")
except Exception as e:
    print(f"Error: {e}")
