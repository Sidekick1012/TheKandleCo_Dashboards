import pandas as pd

EXCEL_FILE = r"c:\Users\aqibr\OneDrive\Desktop\The_Kandle_c0_Dashboard\The Kandle Co. Notes Working 2024-2025.xlsx"

try:
    print("Reading 'Notes' sheet completely...")
    # Read without header to catch everything
    df = pd.read_excel(EXCEL_FILE, sheet_name='Notes', header=None)
    
    # Print first 50 rows to manually inspect structure
    print(df.head(50).to_string())
    
    # Search for keywords like "Sales", "Total", "Revenue", "July", "August"
    print("\n--- KEYWORD SEARCH ---")
    keywords = ['sales', 'total', 'revenue', 'july', 'august', 'september', 'sep', 'aug', 'jul']
    
    found = False
    for i, row in df.iterrows():
        row_str = str(row.values).lower()
        if any(k in row_str for k in keywords):
            print(f"Row {i}: {row.values}")
            found = True
            
    if not found:
        print("No obvious sales keywords found in first scan.")

except Exception as e:
    print(f"Error: {e}")
