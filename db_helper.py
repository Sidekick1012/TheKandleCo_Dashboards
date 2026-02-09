"""
PostgreSQL Database Helper - View tables and insert data
"""

import psycopg2
import os
import sys
import streamlit as st
from dotenv import load_dotenv

# Fix encoding for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Load environment variables
load_dotenv()

# Get database config - Support Secrets and Env
def get_db_config():
    try:
        if hasattr(st, "secrets") and "DB_HOST" in st.secrets:
            return {
                'host': st.secrets["DB_HOST"],
                'port': str(st.secrets.get("DB_PORT", "5432")),
                'database': st.secrets["DB_NAME"],
                'user': st.secrets["DB_USER"],
                'password': st.secrets["DB_PASSWORD"]
            }
    except Exception:
        pass
        
    return {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '5432'),
        'database': os.getenv('DB_NAME', 'kandle_db'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', '')
    }

DB_CONFIG = get_db_config()

def show_all_tables():
    """Show all tables in the database"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        
        tables = cursor.fetchall()
        
        print("\n" + "="*50)
        print(f"Tables in database: {DB_CONFIG['database']}")
        print("="*50)
        
        if not tables:
            print("[!] No tables found in database")
        else:
            for i, (table_name,) in enumerate(tables, 1):
                print(f"{i}. {table_name}")
        
        cursor.close()
        conn.close()
        
        return [t[0] for t in tables]
        
    except Exception as e:
        print(f"[-] Error: {e}")
        return []

def show_table_structure(table_name):
    """Show structure of a specific table"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Get column information
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = %s
            ORDER BY ordinal_position;
        """, (table_name,))
        
        columns = cursor.fetchall()
        
        print("\n" + "="*50)
        print(f"Structure of table: {table_name}")
        print("="*50)
        print(f"{'Column Name':<20} {'Type':<15} {'Nullable'}")
        print("-"*50)
        
        for col_name, data_type, is_nullable in columns:
            print(f"{col_name:<20} {data_type:<15} {is_nullable}")
        
        cursor.close()
        conn.close()
        
        return columns
        
    except Exception as e:
        print(f"[-] Error: {e}")
        return []

def show_table_data(table_name, limit=10):
    """Show data from a table"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Get data
        cursor.execute(f"SELECT * FROM {table_name} LIMIT %s;", (limit,))
        rows = cursor.fetchall()
        
        # Get column names
        col_names = [desc[0] for desc in cursor.description]
        
        print("\n" + "="*50)
        print(f"Data from table: {table_name} (showing {limit} rows)")
        print("="*50)
        
        if not rows:
            print("[!] No data found in table")
        else:
            # Print header
            print(" | ".join(col_names))
            print("-"*50)
            
            # Print rows
            for row in rows:
                print(" | ".join(str(val) for val in row))
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"[-] Error: {e}")

def generate_insert_query(table_name):
    """Generate INSERT query template for a table"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Get columns (excluding auto-increment columns)
        cursor.execute("""
            SELECT column_name, data_type, column_default
            FROM information_schema.columns
            WHERE table_name = %s
            AND column_default NOT LIKE 'nextval%%'
            ORDER BY ordinal_position;
        """, (table_name,))
        
        columns = cursor.fetchall()
        
        print("\n" + "="*50)
        print(f"INSERT Query Template for: {table_name}")
        print("="*50)
        
        # Generate query
        col_names = [col[0] for col in columns if not col[2] or 'CURRENT_TIMESTAMP' not in str(col[2])]
        
        query = f"INSERT INTO {table_name} ("
        query += ", ".join(col_names)
        query += ") \nVALUES ("
        query += ", ".join(["%s"] * len(col_names))
        query += ");"
        
        print("\n-- SQL Query:")
        print(query)
        
        print("\n-- Python Example:")
        print(f"cursor.execute('''")
        print(f"    {query.replace('%s', '%s')}")
        print(f"''', ({', '.join(['value' + str(i+1) for i in range(len(col_names))])}))")
        
        print("\n-- Column Details:")
        for col_name, data_type, _ in columns:
            if col_name in col_names:
                print(f"  {col_name} ({data_type})")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"[-] Error: {e}")

def main():
    print("="*50)
    print("PostgreSQL Database Helper")
    print("="*50)
    
    # Show all tables
    tables = show_all_tables()
    
    if not tables:
        print("\n[!] No tables found. Exiting...")
        return
    
    print("\n")
    print("Choose an option:")
    print("1. View table structure")
    print("2. View table data")
    print("3. Generate INSERT query template")
    print("0. Exit")
    
    choice = input("\nEnter choice (0-3): ").strip()
    
    if choice == "0":
        print("Goodbye!")
        return
    
    if choice in ["1", "2", "3"]:
        table_name = input("\nEnter table name: ").strip()
        
        if table_name not in tables:
            print(f"[-] Table '{table_name}' not found!")
            return
        
        if choice == "1":
            show_table_structure(table_name)
        elif choice == "2":
            show_table_data(table_name)
        elif choice == "3":
            generate_insert_query(table_name)
    else:
        print("[-] Invalid choice!")

if __name__ == "__main__":
    main()
