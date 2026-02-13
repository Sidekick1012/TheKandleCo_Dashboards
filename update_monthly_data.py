"""
Monthly Data Update Script for Neon Database

This script helps you add new monthly data to your Neon database.
You can either:
1. Update local PostgreSQL then sync to Neon
2. Import directly from Excel to Neon
"""

import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

# NEON DATABASE CREDENTIALS (from your migrate_to_cloud.py)
NEON_DB = {
    'host': 'ep-late-water-aiygvdom-pooler.c-4.us-east-1.aws.neon.tech',
    'port': '5432',
    'database': 'neondb',
    'user': 'neondb_owner',
    'password': 'npg_57zhogBbOGvA'
}

# LOCAL DATABASE CREDENTIALS
LOCAL_DB = {
    'host': 'localhost',
    'port': '5432',
    'database': 'The_Kandle_CO',
    'user': 'postgres',
    'password': '1012'
}


def method1_sync_local_to_neon():
    """
    METHOD 1: Update local database first, then sync to Neon
    
    Steps:
    1. Add new month data to local PostgreSQL (using Excel import or manual insert)
    2. Run this function to sync everything to Neon
    """
    print("\n🔄 METHOD 1: Syncing Local → Neon")
    print("="*60)
    
    try:
        local_conn = psycopg2.connect(**LOCAL_DB)
        neon_conn = psycopg2.connect(**NEON_DB)
        
        local_cur = local_conn.cursor()
        neon_cur = neon_conn.cursor()
        
        print("✅ Connected to both databases")
        
        # Tables to sync
        tables = [
            'sales_master', 'profit_loss_summary', 'stockist_sales_detail',
            'commission_details', 'administrative_expenses', 'cash_bank_balances',
            'advertising_breakdown', 'salary_details', 'accounts_payable',
            'accounts_receivable', 'custom_orders', 'cost_of_sales', 'loans'
        ]
        
        for table in tables:
            print(f"\n📊 Syncing: {table}")
            
            # Get data from local
            local_cur.execute(f"SELECT * FROM {table}")
            rows = local_cur.fetchall()
            col_names = [desc[0] for desc in local_cur.description]
            
            # Clear Neon table
            neon_cur.execute(f"DELETE FROM {table}")
            
            # Insert into Neon
            if rows:
                cols = ', '.join(col_names)
                placeholders = ', '.join(['%s'] * len(col_names))
                insert_query = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"
                neon_cur.executemany(insert_query, rows)
                print(f"   ✅ Synced {len(rows)} rows")
            else:
                print(f"   ⚠️ No data in local table")
        
        neon_conn.commit()
        print("\n✨ Sync completed successfully!")
        
        local_conn.close()
        neon_conn.close()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")


def method2_import_excel_to_neon(excel_file_path):
    """
    METHOD 2: Import new month data directly from Excel to Neon
    
    Args:
        excel_file_path: Path to your Excel file with monthly data
    
    Excel should have sheets named after tables:
    - sales_master
    - profit_loss_summary
    - stockist_sales_detail
    etc.
    """
    print("\n📁 METHOD 2: Importing Excel → Neon")
    print("="*60)
    
    try:
        neon_conn = psycopg2.connect(**NEON_DB)
        neon_cur = neon_conn.cursor()
        
        print(f"✅ Connected to Neon")
        print(f"📂 Reading file: {excel_file_path}")
        
        # Read all sheets
        excel_data = pd.read_excel(excel_file_path, sheet_name=None)
        
        for sheet_name, df in excel_data.items():
            print(f"\n📊 Processing sheet: {sheet_name}")
            
            if df.empty:
                print(f"   ⚠️ Sheet is empty, skipping")
                continue
            
            # Prepare data
            columns = df.columns.tolist()
            values = df.values.tolist()
            
            # Insert into Neon
            cols = ', '.join(columns)
            placeholders = ', '.join(['%s'] * len(columns))
            insert_query = f"INSERT INTO {sheet_name} ({cols}) VALUES ({placeholders})"
            
            neon_cur.executemany(insert_query, values)
            print(f"   ✅ Inserted {len(values)} rows")
        
        neon_conn.commit()
        print("\n✨ Import completed successfully!")
        
        neon_conn.close()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")


def method3_add_specific_month(month_name, year):
    """
    METHOD 3: Add specific month data interactively
    
    This will guide you through adding data for a specific month
    """
    print(f"\n➕ METHOD 3: Adding data for {month_name} {year}")
    print("="*60)
    
    try:
        neon_conn = psycopg2.connect(**NEON_DB)
        neon_cur = neon_conn.cursor()
        
        print("✅ Connected to Neon")
        print("\nThis is a template. You'll need to customize it for your data.")
        print("Example: Adding to sales_master table")
        
        # Example for sales_master
        month_year = f"{month_name}-{year}"
        
        print(f"\nTo add {month_year} data:")
        print("1. Prepare your data in Excel")
        print("2. Use method2_import_excel_to_neon()")
        print("Or manually insert using SQL")
        
        neon_conn.close()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")


def view_latest_months():
    """Check what months are already in Neon"""
    print("\n📅 Checking existing months in Neon")
    print("="*60)
    
    try:
        neon_conn = psycopg2.connect(**NEON_DB)
        neon_cur = neon_conn.cursor()
        
        neon_cur.execute("SELECT DISTINCT month FROM sales_master ORDER BY id DESC")
        months = neon_cur.fetchall()
        
        print("\nMonths in database:")
        for month in months:
            print(f"  • {month[0]}")
        
        neon_conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("🗄️  MONTHLY DATA UPDATE FOR NEON DATABASE")
    print("="*60)
    
    print("\nChoose a method:")
    print("\n1️⃣  Sync from Local PostgreSQL to Neon")
    print("    (Update local first, then sync)")
    
    print("\n2️⃣  Import Excel directly to Neon")
    print("    (Have Excel file ready)")
    
    print("\n3️⃣  View existing months")
    
    print("\n0️⃣  Exit")
    
    choice = input("\nEnter choice (0-3): ").strip()
    
    if choice == "1":
        confirm = input("\n⚠️  This will REPLACE all Neon data with local data. Continue? (yes/no): ")
        if confirm.lower() == 'yes':
            method1_sync_local_to_neon()
    
    elif choice == "2":
        excel_path = input("\nEnter Excel file path: ").strip()
        if os.path.exists(excel_path):
            method2_import_excel_to_neon(excel_path)
        else:
            print(f"❌ File not found: {excel_path}")
    
    elif choice == "3":
        view_latest_months()
    
    elif choice == "0":
        print("\n👋 Goodbye!")
    
    else:
        print("\n❌ Invalid choice!")
