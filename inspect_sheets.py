import pandas as pd

EXCEL_FILE = r"c:\Users\aqibr\OneDrive\Desktop\The_Kandle_c0_Dashboard\The Kandle Co. Notes Working 2024-2025.xlsx"

try:
    print("Reading 'Notes' sheet...")
    df = pd.read_excel(EXCEL_FILE, sheet_name='Notes')
    print(df.head(20).to_string())
    
    print("\nReading 'Manufacturing Cost Data' sheet...")
    df2 = pd.read_excel(EXCEL_FILE, sheet_name='Manufacturing Cost Data')
    print(df2.head(20).to_string())

except Exception as e:
    print(f"Error: {e}")
