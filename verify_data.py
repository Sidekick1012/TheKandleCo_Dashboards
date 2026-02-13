"""
Data Verification Tool: Compare Excel vs Neon Database
This script compares your Excel data with Neon database to ensure accuracy
"""

import pandas as pd
import psycopg2
from psycopg2 import sql

# NEON DATABASE CREDENTIALS
NEON_DB = {
    'host': 'ep-late-water-aiygvdom-pooler.c-4.us-east-1.aws.neon.tech',
    'port': '5432',
    'database': 'neondb',
    'user': 'neondb_owner',
    'password': 'npg_57zhogBbOGvA'
}


def compare_excel_with_database(excel_file_path):
    """
    Compare Excel data with Neon database
    Shows differences if any
    """
    print("\n" + "="*70)
    print("📊 DATA VERIFICATION: Excel vs Database")
    print("="*70)
    
    try:
        # Connect to Neon
        conn = psycopg2.connect(**NEON_DB)
        cur = conn.cursor()
        print("✅ Connected to Neon database")
        
        # Read Excel file
        excel_sheets = pd.read_excel(excel_file_path, sheet_name=None)
        print(f"✅ Loaded Excel file: {excel_file_path}")
        print(f"   Found {len(excel_sheets)} sheets\n")
        
        all_match = True
        
        for sheet_name, excel_df in excel_sheets.items():
            print(f"\n{'='*70}")
            print(f"Checking: {sheet_name}")
            print(f"{'='*70}")
            
            # Get data from database
            try:
                cur.execute(f"SELECT * FROM {sheet_name}")
                db_rows = cur.fetchall()
                col_names = [desc[0] for desc in cur.description]
                db_df = pd.DataFrame(db_rows, columns=col_names)
                
                # Compare row counts
                excel_rows = len(excel_df)
                db_rows_count = len(db_df)
                
                print(f"Excel rows: {excel_rows}")
                print(f"Database rows: {db_rows_count}")
                
                if excel_rows != db_rows_count:
                    print(f"⚠️  ROW COUNT MISMATCH!")
                    print(f"   Difference: {abs(excel_rows - db_rows_count)} rows")
                    all_match = False
                    continue
                
                # Compare data
                if excel_rows > 0:
                    # Sort both for comparison
                    excel_sorted = excel_df.sort_values(by=excel_df.columns[0]).reset_index(drop=True)
                    db_sorted = db_df.sort_values(by=db_df.columns[0]).reset_index(drop=True)
                    
                    # Check if all values match
                    differences = []
                    for col in excel_sorted.columns:
                        if col in db_sorted.columns:
                            for idx in range(len(excel_sorted)):
                                excel_val = excel_sorted.loc[idx, col]
                                db_val = db_sorted.loc[idx, col]
                                
                                # Handle float comparison
                                if pd.isna(excel_val) and pd.isna(db_val):
                                    continue
                                elif str(excel_val).strip() != str(db_val).strip():
                                    differences.append({
                                        'row': idx + 1,
                                        'column': col,
                                        'excel': excel_val,
                                        'database': db_val
                                    })
                    
                    if differences:
                        print(f"❌ DATA MISMATCH! Found {len(differences)} differences:")
                        for diff in differences[:10]:  # Show first 10
                            print(f"\n   Row {diff['row']}, Column '{diff['column']}':")
                            print(f"   Excel:    {diff['excel']}")
                            print(f"   Database: {diff['database']}")
                        all_match = False
                    else:
                        print("✅ ALL DATA MATCHES PERFECTLY!")
                else:
                    print("✅ Both Excel and Database are empty")
                    
            except Exception as e:
                print(f"⚠️  Error checking {sheet_name}: {e}")
                all_match = False
        
        conn.close()
        
        # Final Summary
        print("\n\n" + "="*70)
        print("📋 VERIFICATION SUMMARY")
        print("="*70)
        
        if all_match:
            print("✅ ✅ ✅ PERFECT MATCH! ✅ ✅ ✅")
            print("\nYour Excel data and Neon Database are EXACTLY THE SAME!")
            print("No changes, no differences - 100% accurate! 💯")
        else:
            print("⚠️  MISMATCHES FOUND!")
            print("\nSome data differences detected between Excel and Database.")
            print("Please review the details above.")
        
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")


def quick_summary():
    """Quick summary of database contents"""
    print("\n" + "="*70)
    print("📊 NEON DATABASE QUICK SUMMARY")
    print("="*70)
    
    try:
        conn = psycopg2.connect(**NEON_DB)
        cur = conn.cursor()
        
        # Get all tables
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema='public'
            ORDER BY table_name
        """)
        tables = [t[0] for t in cur.fetchall()]
        
        print(f"\nTotal Tables: {len(tables)}\n")
        
        total_rows = 0
        for table in tables:
            cur.execute(f"SELECT COUNT(*) FROM {table}")
            count = cur.fetchone()[0]
            total_rows += count
            print(f"  • {table:<30} {count:>6} rows")
        
        print(f"\n{'Total Rows:':<32} {total_rows:>6}")
        print("="*70 + "\n")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("🔍 DATA VERIFICATION TOOL")
    print("="*70)
    
    print("\nChoose an option:")
    print("\n1️⃣  Compare Excel file with Database")
    print("2️⃣  Show Database summary")
    print("\n0️⃣  Exit")
    
    choice = input("\nEnter choice: ").strip()
    
    if choice == "1":
        excel_path = input("\nEnter Excel file path: ").strip()
        import os
        if os.path.exists(excel_path):
            compare_excel_with_database(excel_path)
        else:
            print(f"\n❌ File not found: {excel_path}")
    
    elif choice == "2":
        quick_summary()
    
    elif choice == "0":
        print("\n👋 Goodbye!")
    
    else:
        print("\n❌ Invalid choice!")
