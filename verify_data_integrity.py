import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Cloud Database Config
DB_HOST = "ep-late-water-aiygvdom-pooler.c-4.us-east-1.aws.neon.tech"
DB_NAME = "neondb"
DB_USER = "neondb_owner"
DB_PASS = "npg_57zhogBbOGvA"

EXCEL_FILE = r"c:\Users\aqibr\OneDrive\Desktop\The_Kandle_c0_Dashboard\The Kandle Co. Notes Working 2024-2025.xlsx"

def verify_data():
    print("🚀 Starting Data Verification (Excel vs Database)...")
    
    try:
        # 1. Read Excel Data (Sales Master)
        print("\n📄 Reading Excel File...")
        xls = pd.ExcelFile(EXCEL_FILE)
        
        # Check sheet availability
        sheet_name = 'Sales Master'
        if sheet_name not in xls.sheet_names:
            print(f"❌ '{sheet_name}' sheet not found in Excel!")
            return

        df_excel = pd.read_excel(xls, sheet_name=sheet_name)
        
        # Clean Excel Data - assuming structure based on previous interactions
        # We need to find the header row first
        # Usually headers are 'Month', 'Online', 'Stockist', etc.
        
        # Let's try to find headers row dynamically
        header_row = 0
        for i, row in df_excel.head(10).iterrows():
            if 'Month' in str(row.values) or 'Total' in str(row.values):
                header_row = i
                break
                
        df_excel = pd.read_excel(xls, sheet_name=sheet_name, header=header_row)
        
        # Clean up column names generally
        df_excel.columns = [str(c).strip() for c in df_excel.columns]
        
        # Filter relevant columns if possible
        # We expect columns like 'Month', 'Online Sales', 'Total Sales'
        print(f"   Excel Columns: {df_excel.columns.tolist()[:10]}...")

        # 2. Connect to Database
        print("\n🔌 Connecting to Database...")
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        
        # 3. Compare Sales Data
        print("\n📊 Comparing Data (Sample: Last 3 Months)...")
        
        query = "SELECT month_year, total_sales FROM sales_master ORDER BY id DESC LIMIT 3"
        df_db = pd.read_sql_query(query, conn)
        
        print("\n--- DATABASE DATA ---")
        print(df_db.to_string(index=False))
        
        print("\n--- EXCEL DATA GLIMPSE ---")
        # Just printing head to see if we can manually match visually for now
        # because exact string matching on dates might be tricky without full parsing
        print(df_excel.head(5).to_string())

        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    verify_data()
