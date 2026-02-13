import psycopg2
import pandas as pd

NEON_DB = {
    'host': 'ep-late-water-aiygvdom-pooler.c-4.us-east-1.aws.neon.tech',
    'port': '5432',
    'database': 'neondb',
    'user': 'neondb_owner',
    'password': 'npg_57zhogBbOGvA'
}

conn = psycopg2.connect(**NEON_DB)

print("Checking stockist_sales_detail table:\n")

# Check for empty/null channel names
query = """
SELECT channel, SUM(amount) as total_sales
FROM stockist_sales_detail
GROUP BY channel
ORDER BY total_sales DESC
LIMIT 10
"""

df = pd.read_sql(query, conn)
print(df.to_string())

print("\n\nChecking for empty or null channel names:")
query2 = "SELECT COUNT(*) FROM stockist_sales_detail WHERE channel IS NULL OR channel = ''"
cur = conn.cursor()
cur.execute(query2)
print(f"Empty/Null channels: {cur.fetchone()[0]}")

conn.close()
