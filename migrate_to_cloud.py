import psycopg2
import os
from dotenv import load_dotenv

# Load local environment variables
load_dotenv()

# LOCAL DATABASE CONFIG (Fetched from your .env)
LOCAL_DB = {
    'host': 'localhost',
    'port': '5432',
    'database': 'The_Kandle_CO',
    'user': 'postgres',
    'password': '1012'
}

# CLOUD DATABASE CONFIG (Updated from your screenshot)
CLOUD_DB = {
    'host': 'ep-late-water-aiygvdom-pooler.c-4.us-east-1.aws.neon.tech',
    'port': '5432',
    'database': 'neondb',
    'user': 'neondb_owner',
    'password': 'npg_57zhogBbOGvA' # Masked in screenshot
}

def migrate():
    print("🚀 Starting Data Migration to Cloud...")
    
    try:
        # 1. Connect to Local
        local_conn = psycopg2.connect(**LOCAL_DB)
        local_cur = local_conn.cursor()
        print("[+] Connected to Local Database")
        
        # 2. Connect to Cloud
        cloud_conn = psycopg2.connect(**CLOUD_DB)
        cloud_cur = cloud_conn.cursor()
        print("[+] Connected to Cloud Database")
        
        # 3. List tables to migrate
        tables = [
            'users',
            'sales_master',
            'profit_loss_summary',
            'stockist_sales_detail',
            'commission_details',
            'administrative_expenses',
            'cash_bank_balances',
            'advertising_breakdown',
            'salary_details',
            'accounts_payable',
            'accounts_receivable',
            'custom_orders'
        ]
        
        for table in tables:
            print(f"📦 Migrating table: {table}")
            
            # Get data and metadata from local
            try:
                local_cur.execute(f"SELECT * FROM {table}")
                rows = local_cur.fetchall()
                # Get column info
                desc = local_cur.description
                colnames = [d[0] for d in desc]
            except Exception as e:
                print(f"   [!] Skipping {table}: {e}")
                local_conn.rollback()
                continue
            
            # 1. Create table in cloud (Inferred Schema)
            # This is a basic mapping, works for common types
            type_map = {
                16: 'BOOLEAN', 20: 'BIGINT', 21: 'SMALLINT', 23: 'INTEGER',
                700: 'REAL', 701: 'DOUBLE PRECISION', 1042: 'CHAR', 1043: 'VARCHAR(255)',
                1114: 'TIMESTAMP', 1184: 'TIMESTAMPTZ', 1082: 'DATE', 1700: 'NUMERIC'
            }
            
            col_defs = []
            for d in desc:
                name = d[0]
                type_oid = d[1]
                sql_type = type_map.get(type_oid, 'TEXT')
                col_defs.append(f"{name} {sql_type}")
            
            create_sql = f"CREATE TABLE IF NOT EXISTS {table} ({', '.join(col_defs)})"
            cloud_cur.execute(create_sql)
            if table == 'users':
                cloud_cur.execute('CREATE INDEX IF NOT EXISTS idx_username ON users(username)')
            print(f"   [+] Table {table} schema verified/created")

            # 2. Clear and Insert
            cols = ', '.join(colnames)
            placeholders = ', '.join(['%s'] * len(colnames))
            
            cloud_cur.execute(f"DELETE FROM {table}")
            insert_query = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"
            cloud_cur.executemany(insert_query, rows)
            
            print(f"✅ Successfully migrated {len(rows)} rows for {table}")
            
        cloud_conn.commit()
        print("\n✨ Migration Completed Successfully!")
        
    except Exception as e:
        print(f"\n❌ Migration Failed: {e}")
    finally:
        if 'local_conn' in locals(): local_conn.close()
        if 'cloud_conn' in locals(): cloud_conn.close()

if __name__ == "__main__":
    print("--- The Kandle Co. Database Migrator ---")
    migrate()
