import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def check_db():
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        cur = conn.cursor()
        
        # Get all tables
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
        tables = [t[0] for t in cur.fetchall()]
        
        for table in tables:
            print(f"\n--- Table: {table} ---")
            # Get columns
            cur.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name='{table}'")
            cols = cur.fetchall()
            for col in cols:
                print(f"  {col[0]} ({col[1]})")
            
            # Get row count
            cur.execute(f"SELECT COUNT(*) FROM {table}")
            count = cur.fetchone()[0]
            print(f"  Row Count: {count}")
            
            if count > 0:
                print("  Sample Data (1 row):")
                cur.execute(f"SELECT * FROM {table} LIMIT 1")
                print(f"    {cur.fetchone()}")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    check_db()
