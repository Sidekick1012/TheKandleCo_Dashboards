import pandas as pd

# Read the Excel file
excel_file = r"c:\Users\aqibr\OneDrive\Desktop\The_Kandle_c0_Dashboard\The Kandle Co. Notes Working 2024-2025.xlsx"

try:
    # Read Items sheet
    print("=" * 60)
    print("ITEMS/PRODUCTS:")
    print("=" * 60)
    df_items = pd.read_excel(excel_file, sheet_name='Items Name & Price')
    print(df_items.to_string())
    
    print("\n" + "=" * 60)
    print("CGS SHEET (First 30 rows):")
    print("=" * 60)
    df_cgs = pd.read_excel(excel_file, sheet_name='CGS', header=None)
    print(df_cgs.head(30).to_string())
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
