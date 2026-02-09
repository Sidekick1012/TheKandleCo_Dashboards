"""
Excel File Analyzer - See what's inside the Excel file
"""

import pandas as pd
import sys
import os

# Fix encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def analyze_excel(file_path):
    """Analyze Excel file structure"""
    print("="*60)
    print(f"Analyzing: {os.path.basename(file_path)}")
    print("="*60)
    
    try:
        # Read Excel file
        excel_file = pd.ExcelFile(file_path)
        
        print(f"\n[+] Found {len(excel_file.sheet_names)} sheet(s):")
        
        for i, sheet_name in enumerate(excel_file.sheet_names, 1):
            print(f"\n{i}. Sheet: '{sheet_name}'")
            print("-"*60)
            
            # Read sheet
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            
            print(f"   Rows: {len(df)}")
            print(f"   Columns: {len(df.columns)}")
            
            print(f"\n   Column Names & Types:")
            for col in df.columns:
                dtype = df[col].dtype
                non_null = df[col].count()
                print(f"      - {col:<30} ({dtype}, {non_null}/{len(df)} non-null)")
            
            print(f"\n   First 3 rows preview:")
            print(df.head(3).to_string(index=False))
            print()
        
        return excel_file
        
    except Exception as e:
        print(f"[-] Error: {e}")
        return None

if __name__ == "__main__":
    file_path = "The Kandle Co. Notes Working 2024-2025.xlsx"
    analyze_excel(file_path)
