import psycopg2

NEON_DB = {
    'host': 'ep-late-water-aiygvdom-pooler.c-4.us-east-1.aws.neon.tech',
    'port': '5432',
    'database': 'neondb',
    'user': 'neondb_owner',
    'password': 'npg_57zhogBbOGvA'
}

conn = psycopg2.connect(**NEON_DB)
cur = conn.cursor()

# Get all tables
cur.execute("""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public'
    ORDER BY table_name
""")

tables = cur.fetchall()
print("=" * 50)
print("DATABASE TABLES:")
print("=" * 50)
for table in tables:
    print(f"  - {table[0]}")

print("\n" + "=" * 50)
print("SAMPLE DATA FROM KEY TABLES:")
print("=" * 50)

# Check custom_orders for customers
print("\n1. CUSTOM ORDERS (Customers):")
cur.execute("SELECT customer_name, total_rev FROM custom_orders LIMIT 5")
for row in cur.fetchall():
    print(f"   {row[0]}: Rs. {row[1]:,.0f}")

# Check stockist_sales_detail for stockists
print("\n2. STOCKIST SALES (Stockists/Partners):")
cur.execute("SELECT DISTINCT stockist_name FROM stockist_sales_detail WHERE stockist_name IS NOT NULL LIMIT 10")
for row in cur.fetchall():
    print(f"   - {row[0]}")

# Check if there's product/item data
print("\n3. Checking for product tables...")
cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND (table_name LIKE '%item%' OR table_name LIKE '%product%')")
product_tables = cur.fetchall()
if product_tables:
    for table in product_tables:
        print(f"   Found: {table[0]}")
else:
    print("   No product tables found")

conn.close()
