"""
Direct SQL Query Tool for Neon Database
Run custom INSERT/UPDATE/SELECT queries on Neon
"""

import psycopg2
from psycopg2 import sql

# NEON DATABASE CREDENTIALS
NEON_DB = {
    'host': 'ep-late-water-aiygvdom-pooler.c-4.us-east-1.aws.neon.tech',
    'port': '5432',
    'database': 'neondb',
    'user': 'neondb_owner',
    'password': 'npg_57zhogBbOGvA'
}


def run_query(query, params=None, fetch=False):
    """Execute a SQL query on Neon database"""
    try:
        conn = psycopg2.connect(**NEON_DB)
        cur = conn.cursor()
        
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
        
        if fetch:
            results = cur.fetchall()
            col_names = [desc[0] for desc in cur.description] if cur.description else []
            conn.close()
            return results, col_names
        else:
            conn.commit()
            rows_affected = cur.rowcount
            conn.close()
            return rows_affected
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def insert_sales_master(month, total_sales, cash_position=1.00):
    """
    Quick insert into sales_master table
    Example: insert_sales_master('Jul-2025', 2500000.00)
    """
    query = """
    INSERT INTO sales_master (month, total_sales, cash_position) 
    VALUES (%s, %s, %s)
    """
    rows = run_query(query, (month, total_sales, cash_position))
    if rows:
        print(f"✅ Inserted {rows} row into sales_master")
    return rows


def insert_stockist_sales(month_id, month, channel, amount, percentage):
    """
    Quick insert into stockist_sales_detail
    Example: insert_stockist_sales(44, 'Jul-2025', 'Sales Shams', 500000.00, 0.20)
    """
    query = """
    INSERT INTO stockist_sales_detail (month_id, month, channel, amount, percentage) 
    VALUES (%s, %s, %s, %s, %s)
    """
    rows = run_query(query, (month_id, month, channel, amount, percentage))
    if rows:
        print(f"✅ Inserted {rows} row into stockist_sales_detail")
    return rows


def run_custom_query():
    """Interactive mode - run any custom SQL query"""
    print("\n" + "="*70)
    print("📝 CUSTOM SQL QUERY MODE")
    print("="*70)
    print("\nEnter your SQL query (type 'exit' to quit)")
    print("For multi-line queries, end with semicolon ;")
    print("\nExamples:")
    print("  SELECT * FROM sales_master WHERE month = 'Jul-2025';")
    print("  INSERT INTO sales_master (month, total_sales) VALUES ('Jul-2025', 2500000);")
    print("  UPDATE sales_master SET cash_position = 1.00 WHERE month = 'Jul-2025';")
    print("-"*70 + "\n")
    
    while True:
        query = input("SQL> ").strip()
        
        if query.lower() == 'exit':
            print("👋 Goodbye!")
            break
        
        if not query:
            continue
        
        # Determine if it's a SELECT query
        is_select = query.upper().startswith('SELECT')
        
        if is_select:
            result = run_query(query, fetch=True)
            if result:
                rows, col_names = result
                if col_names:
                    print("\n" + " | ".join(col_names))
                    print("-" * 70)
                for row in rows:
                    print(" | ".join(str(val) for val in row))
                print(f"\n✅ {len(rows)} rows returned\n")
        else:
            rows_affected = run_query(query)
            if rows_affected is not None:
                print(f"\n✅ Query executed. {rows_affected} rows affected.\n")


def show_table_templates():
    """Show INSERT query templates for all tables"""
    templates = {
        "sales_master": """
INSERT INTO sales_master (month, total_sales, cash_position) 
VALUES ('Jul-2025', 2500000.00, 1.00);
        """,
        
        "profit_loss_summary": """
INSERT INTO profit_loss_summary (month, revenue, cogs, gross_profit, gross_margin, 
                                  admin_expenses, advertising, net_profit, net_margin) 
VALUES ('Jul-2025', 2500000, 600000, 1900000, 0.76, 
        300000, 150000, 1450000, 0.58);
        """,
        
        "stockist_sales_detail": """
INSERT INTO stockist_sales_detail (month_id, month, channel, amount, percentage) 
VALUES (44, 'Jul-2025', 'Sales Shams', 500000.00, 0.20);
        """,
        
        "commission_details": """
INSERT INTO commission_details (month, stockist, amount) 
VALUES ('Jul-2025', 'Sales Shams', 25000.00);
        """,
        
        "administrative_expenses": """
INSERT INTO administrative_expenses (month, rent, utilities, salaries, other, total) 
VALUES ('Jul-2025', 50000, 10000, 200000, 40000, 300000);
        """,
        
        "advertising_breakdown": """
INSERT INTO advertising_breakdown (month, platform, amount) 
VALUES ('Jul-2025', 'Social Media', 50000.00);
        """,
        
        "salary_details": """
INSERT INTO salary_details (month, employee, salary) 
VALUES ('Jul-2025', 'Manager', 80000.00);
        """
    }
    
    print("\n" + "="*70)
    print("📋 INSERT QUERY TEMPLATES")
    print("="*70)
    
    for table, template in templates.items():
        print(f"\n--- {table.upper()} ---")
        print(template.strip())
    
    print("\n" + "="*70)


def main():
    print("\n" + "="*70)
    print("🗄️  NEON DATABASE - SQL QUERY TOOL")
    print("="*70)
    print("\nChoose an option:")
    print("\n1️⃣  Run custom SQL queries (Interactive)")
    print("2️⃣  View INSERT templates")
    print("3️⃣  Quick add to sales_master")
    print("4️⃣  Quick add to stockist_sales_detail")
    print("5️⃣  View existing months")
    print("\n0️⃣  Exit")
    
    choice = input("\nEnter choice: ").strip()
    
    if choice == "1":
        run_custom_query()
    
    elif choice == "2":
        show_table_templates()
    
    elif choice == "3":
        month = input("Month (e.g., Jul-2025): ").strip()
        sales = float(input("Total Sales: "))
        cash_pos = float(input("Cash Position (default 1.00): ") or "1.00")
        insert_sales_master(month, sales, cash_pos)
    
    elif choice == "4":
        month_id = int(input("Month ID: "))
        month = input("Month (e.g., Jul-2025): ").strip()
        channel = input("Channel name: ").strip()
        amount = float(input("Amount: "))
        percentage = float(input("Percentage (decimal, e.g., 0.20): "))
        insert_stockist_sales(month_id, month, channel, amount, percentage)
    
    elif choice == "5":
        results, cols = run_query("SELECT DISTINCT month FROM sales_master ORDER BY id DESC", fetch=True)
        print("\n📅 Months in database:")
        for row in results:
            print(f"  • {row[0]}")
    
    elif choice == "0":
        print("\n👋 Goodbye!")
    
    else:
        print("\n❌ Invalid choice!")


if __name__ == "__main__":
    main()
