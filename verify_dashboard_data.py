from data_utils import get_monthly_sales_trend, get_all_customers, get_custom_orders, get_db_connection

print("🚀 Verifying Dashboard Data Fetching...")

conn = get_db_connection()
if conn:
    print("✅ DB Connection in data_utils WORKED.")
    conn.close()
else:
    print("❌ DB Connection in data_utils FAILED.")

# 1. Monthly Trend (Should show Jul-2024 with ~1.7 Cr)
print("\n📊 Checking Monthly Sales Trend...")
df_trend = get_monthly_sales_trend()
if not df_trend.empty:
    print(df_trend[['month_year', 'total_sales']].to_string(index=False))
else:
    print("❌ No monthly trend data found.")

# 2. Customer Directory (Should show top customers like Kickstart, Shams)
print("\n👥 Checking Customer Directory...")
df_cust = get_all_customers()
if not df_cust.empty:
    print(f"Columns found: {df_cust.columns.tolist()}")
    print(df_cust.head(10)[['customer_name', 'total_revenue']].to_string(index=False))
else:
    print("❌ No customer data found.")

# 3. Custom Orders (Should show individual orders)
print("\n📦 Checking Custom Orders...")
df_orders = get_custom_orders()
if not df_orders.empty:
    print(df_orders.head(5)[['customer_name', 'order_amount']].to_string(index=False))
else:
    print("❌ No custom orders found.")
