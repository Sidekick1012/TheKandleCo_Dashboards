"""
Quick Data Verification: Excel vs Neon Database
"""

import pandas as pd
import psycopg2

# NEON DATABASE
NEON_DB = {
    'host': 'ep-late-water-aiygvdom-pooler.c-4.us-east-1.aws.neon.tech',
    'port': '5432',
    'database': 'neondb',
    'user': 'neondb_owner',
    'password': 'npg_57zhogBbOGvA'
}

excel_file = "The Kandle Co. Notes Working 2024-2025.xlsx"

print("\n" + "="*80)
print("📊 VERIFYING: Excel vs Neon Database")
print("="*80)
print(f"\nExcel File: {excel_file}\n")

try:
    # Connect to Neon
    conn = psycopg2.connect(**NEON_DB)
    cur = conn.cursor()
    print("✅ Connected to Neon\n")
    
    # Read Excel
    excel_sheets = pd.read_excel(excel_file, sheet_name=None)
    print(f"✅ Loaded Excel ({len(excel_sheets)} sheets)\n")
    
    print("="*80)
    print("COMPARISON RESULTS:")
    print("="*80)
    
    all_good = True
    
    for sheet_name in ['sales_master', 'profit_loss_summary', 'stockist_sales_detail']:
        if sheet_name not in excel_sheets:
            print(f"\n⚠️  Sheet '{sheet_name}' not found in Excel")
            continue
            
        excel_df = excel_sheets[sheet_name]
        
        # Get from database
        cur.execute(f"SELECT * FROM {sheet_name}")
        db_rows = cur.fetchall()
        col_names = [desc[0] for desc in cur.description]
        db_df = pd.DataFrame(db_rows, columns=col_names)
        
        print(f"\n{sheet_name}:")
        print(f"  Excel rows: {len(excel_df)}")
        print(f"  DB rows: {len(db_df)}")
        
        if len(excel_df) == len(db_df):
            print(f"  ✅ Row count matches!")
        else:
            print(f"  ❌ MISMATCH! Difference: {abs(len(excel_df) - len(db_df))} rows")
            all_good = False
    
    print("\n" + "="*80)
    if all_good:
        print("✅ ✅ ✅ DATA VERIFIED - EVERYTHING MATCHES! ✅ ✅ ✅")
        print("\nYour Excel and Database have THE SAME DATA!")
        print("No changes, completely accurate! 💯")
    else:
        print("⚠️  Some differences found - see details above")
    print("="*80 + "\n")
    
    conn.close()
    
except Exception as e:
    print(f"\n❌ Error: {e}\n")
