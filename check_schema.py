import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = "ep-late-water-aiygvdom-pooler.c-4.us-east-1.aws.neon.tech"
DB_NAME = "neondb"
DB_USER = "neondb_owner"
DB_PASS = "npg_57zhogBbOGvA"

def check_schema():
    print("🚀 Connecting to Database...")
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        cur = conn.cursor()
        
        # Check custom_orders schema
        print("📄 Checking 'custom_orders' columns...")
        cur.execute("SELECT * FROM custom_orders LIMIT 0")
        colnames = [desc[0] for desc in cur.description]
        print(f"Columns: {colnames}")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_schema()
