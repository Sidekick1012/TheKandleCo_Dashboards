import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

print("Checking DB Connection Variables:")
print(f"DB_HOST: {os.getenv('DB_HOST')}")
print(f"DB_NAME: {os.getenv('DB_NAME')}")
print(f"DB_USER: {os.getenv('DB_USER')}")

print("\nAttempting Connection...")
try:
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        connect_timeout=5
    )
    print("✅ Connection Successful!")
    conn.close()
except Exception as e:
    print(f"❌ Connection Failed: {e}")
