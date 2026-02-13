import pandas as pd

# Read the Excel file
excel_file = r"c:\Users\aqibr\OneDrive\Desktop\The_Kandle_c0_Dashboard\The Kandle Co. Notes Working 2024-2025.xlsx"

try:
    # Get all sheet names
    excel_data = pd.ExcelFile(excel_file)
    print("=" * 60)
    print("AVAILABLE SHEETS:")
    print("=" * 60)
    for i, sheet in enumerate(excel_data.sheet_names, 1):
        print(f"{i}. {sheet}")
    
    print("\n" + "=" * 60)
    print("LOOKING FOR PRODUCT INFORMATION...")
    print("=" * 60)
    
    # Check each sheet for product-related data
    for sheet_name in excel_data.sheet_names:
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        
        # Look for columns that might contain product names
        product_columns = [col for col in df.columns if any(keyword in str(col).lower() 
                          for keyword in ['product', 'item', 'candle', 'diffuser', 'name', 'type'])]
        
        if product_columns:
            print(f"\n📋 SHEET: {sheet_name}")
            print(f"   Possible product columns: {product_columns}")
            print(f"   Total rows: {len(df)}")
            
            # Show sample data from product columns
            for col in product_columns[:3]:  # Show up to 3 columns
                unique_values = df[col].dropna().unique()
                if len(unique_values) > 0 and len(unique_values) < 50:
                    print(f"\n   Column '{col}' unique values ({len(unique_values)}):")
                    for val in unique_values[:15]:  # Show first 15
                        print(f"     - {val}")
                elif len(unique_values) >= 50:
                    print(f"\n   Column '{col}': {len(unique_values)} unique values (too many to list)")

except Exception as e:
    print(f"Error reading Excel file: {e}")
    import traceback
    traceback.print_exc()
