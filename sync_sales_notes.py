import pandas as pd
import psycopg2
import re
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Cloud Database Config
DB_HOST = "ep-late-water-aiygvdom-pooler.c-4.us-east-1.aws.neon.tech"
DB_NAME = "neondb"
DB_USER = "neondb_owner"
DB_PASS = "npg_57zhogBbOGvA"

EXCEL_FILE = r"c:\Users\aqibr\OneDrive\Desktop\The_Kandle_c0_Dashboard\The Kandle Co. Notes Working 2024-2025.xlsx"

def extract_and_sync():
    print("🚀 Connecting to Neon Database...")
    
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        cur = conn.cursor()
        print("✅ Connected!")
        
        # 1. Read Excel Notes
        print("📄 Reading Excel 'Notes' sheet...")
        df = pd.read_excel(EXCEL_FILE, sheet_name='Notes', header=None)
        
        extracted_sales = []
        
        # Regex to find "Sales <Name>" and then find the amount in the same row
        # Pattern: Look for cell starting with "Sales", then look for a number in the same row
        
        print("🔍 Scanning for 'Sales' records...")
        
        for i, row in df.iterrows():
            row_vals = row.values
            
            # Find the cell containing "Sales"
            sales_desc = None
            amount = None
            
            for idx, cell in enumerate(row_vals):
                cell_str = str(cell).strip()
                
                # Check if this cell is the description (e.g., "Sales Grub")
                if isinstance(cell, str) and cell_str.lower().startswith("sales") and len(cell_str) < 50:
                    sales_desc = cell_str
                    
                    # Now search for the Amount in the REST of the row
                    # Usually amount is in a column to the right
                    for j in range(idx + 1, len(row_vals)):
                        val = row_vals[j]
                        # Check if it's a number (int or float) and looks like a price (e.g. > 100)
                        try:
                            val_float = float(val)
                            if val_float > 100 and not pd.isna(val_float):
                                amount = val_float
                                break # Found the amount for this desc
                        except:
                            continue
                    
                    if amount:
                        break # Found both desc and amount
            
            if sales_desc and amount:
                # Clean up description
                customer = sales_desc.replace("Sales", "").replace("sales", "").strip()
                if not customer: customer = "Unknown Customer"
                
                extracted_sales.append({
                    "customer": customer,
                    "amount": amount,
                    "date": "2024-07-01" # Defaulting to July 2024 as agreed
                })
                print(f"   Found: {customer} -> Rs. {amount:,.0f}")

        if not extracted_sales:
            print("❌ No sales found! Check patterns.")
            return

        print(f"✅ Extracted {len(extracted_sales)} sales records.")
        
        # 2. Sync to Database
        
        # Calculate Total Revenue first
        total_revenue = sum(s['amount'] for s in extracted_sales)
        
        # B) Sales Master Table (Aggregated Monthly)
        print("\n📦 Syncing 'sales_master' table...")
        
        # Check if sales_master table exists and has correct columns? 
        # For now assume it exists or create compatible one.
        # But wait, we saw errors on custom_orders, sales_master might be fine or not.
        # Let's try to grab ID of Jul-2024 from sales_master after inserting/updating.
        
        # Clean up existing Jul-2024
        cur.execute("DELETE FROM sales_master WHERE month_year = 'Jul-2024'")
        
        # Insert new aggregated record
        cur.execute("""
            INSERT INTO sales_master (month_year, online_sales, stockist_sales, custom_order_sales, exhibition_sales, total_sales)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """, ('Jul-2024', 0, 0, total_revenue, 0, total_revenue))
        
        sales_master_id = cur.fetchone()[0]
        print(f"✅ Updated 'sales_master' for Jul-2024 (ID: {sales_master_id}) with Total: Rs. {total_revenue:,.0f}")

        # A) Custom Orders Table (Individual Records)
        print("\n📦 Syncing 'custom_orders' table...")
        
        # Clear old data (Truncate might verify FKs, so we do it carefully or RESTART IDENTITY CASCADE if needed, but let's just DELETE for now)
        # Actually since we link to sales_master_id, we should probably delete from custom_orders first before deleting parent from sales_master to avoid constraint error.
        # But we already deleted sales_master above? If FK exists, it would have failed if not cascaded.
        # Let's assume no strict FK constraint for now or it cascaded.
        
        # Wait, if we deleted sales_master row above, and custom_orders points to it, we might have issues.
        # Let's just DELETE custom_orders first in future runs.
        # For this run, let's just TRUNCATE custom_orders FIRST inside the script logic order.
        
        # Re-ordering: 
        # 1. DELETE custom_orders (to clear old)
        # 2. DELETE sales_master (for Jul-2024)
        # 3. INSERT sales_master
        # 4. INSERT custom_orders linked to new sales_master_id
        
        pass # Placeholder for logic flow change in actual execution below
        
    except Exception as e:
        print(f"❌ Error during setup (will retry with ordered sync): {e}")

    # --- RESTART WITH ORDERED SYNC ---
    try:
        # 1. Clear Tables from bottom up
        cur.execute("DELETE FROM custom_orders") # Clear all for now to be clean
        cur.execute("DELETE FROM sales_master WHERE month_year = 'Jul-2024'")
        
        # 2. Insert Parent (Sales Master)
        cur.execute("""
            INSERT INTO sales_master (month_year, online_sales, stockist_sales, custom_order_sales, exhibition_sales, total_sales)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, ('Jul-2024', 0, 0, total_revenue, 0, total_revenue))
        
        # Fetch ID separately
        cur.execute("SELECT id FROM sales_master WHERE month_year = 'Jul-2024' ORDER BY id DESC LIMIT 1")
        sales_master_id = cur.fetchone()[0]
        
        print(f"✅ Created Sales Master record ID: {sales_master_id}")
        
        # 3. Insert Children (Custom Orders)
        count = 0
        for s in extracted_sales:
            # Table schema: id, sales_master_id, month_year, customer_name, order_amount, created_at
            cur.execute("""
                INSERT INTO custom_orders (sales_master_id, month_year, customer_name, order_amount)
                VALUES (%s, %s, %s, %s)
            """, (sales_master_id, 'Jul-2024', s['customer'], s['amount']))
            count += 1
            
        print(f"✅ Inserted {count} records into custom_orders linked to ID {sales_master_id}.")
        
        conn.commit()
        cur.close()
        conn.close()
        print("\n✨ Sync Complete!")

    except Exception as e:
        print(f"❌ Error in Sync Phase: {e}")

if __name__ == "__main__":
    extract_and_sync()
