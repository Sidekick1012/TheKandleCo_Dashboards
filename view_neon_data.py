import psycopg2
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

def view_neon_data():
    """Connect to Neon database and display all data"""
    try:
        # Connect to database
        print("Connecting to database...")
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        cur = conn.cursor()
        
        print(f"\n✅ Connected to: {os.getenv('DB_NAME')} at {os.getenv('DB_HOST')}\n")
        
        # Get all tables
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema='public'
            ORDER BY table_name
        """)
        tables = [t[0] for t in cur.fetchall()]
        
        print(f"Found {len(tables)} tables in database:\n")
        
        for table in tables:
            print(f"\n{'='*80}")
            print(f"TABLE: {table.upper()}")
            print(f"{'='*80}")
            
            # Get column information
            cur.execute(f"""
                SELECT column_name, data_type, character_maximum_length
                FROM information_schema.columns 
                WHERE table_name='{table}'
                ORDER BY ordinal_position
            """)
            columns = cur.fetchall()
            
            print(f"\nColumns ({len(columns)}):")
            for col in columns:
                col_name, data_type, max_length = col
                length_info = f"({max_length})" if max_length else ""
                print(f"  • {col_name}: {data_type}{length_info}")
            
            # Get row count
            cur.execute(f"SELECT COUNT(*) FROM {table}")
            count = cur.fetchone()[0]
            print(f"\nTotal Rows: {count}")
            
            # Display data
            if count > 0:
                print(f"\n--- DATA (showing all {count} rows) ---\n")
                
                # Get all data
                cur.execute(f"SELECT * FROM {table}")
                rows = cur.fetchall()
                col_names = [desc[0] for desc in cur.description]
                
                # Create DataFrame for better display
                df = pd.DataFrame(rows, columns=col_names)
                
                # Display the dataframe
                pd.set_option('display.max_columns', None)
                pd.set_option('display.width', None)
                pd.set_option('display.max_colwidth', 50)
                
                print(df.to_string(index=True))
                print()
            else:
                print("\n--- NO DATA IN THIS TABLE ---\n")
        
        # Summary statistics
        print(f"\n{'='*80}")
        print("DATABASE SUMMARY")
        print(f"{'='*80}")
        print(f"Total Tables: {len(tables)}")
        
        total_rows = 0
        for table in tables:
            cur.execute(f"SELECT COUNT(*) FROM {table}")
            count = cur.fetchone()[0]
            total_rows += count
            print(f"  • {table}: {count} rows")
        
        print(f"\nTotal Rows Across All Tables: {total_rows}")
        
        cur.close()
        conn.close()
        print(f"\n✅ Connection closed successfully")
        
    except Exception as e:
        print(f"\n❌ Error connecting to database: {e}")
        print(f"\nDatabase Configuration:")
        print(f"  Host: {os.getenv('DB_HOST')}")
        print(f"  Port: {os.getenv('DB_PORT')}")
        print(f"  Database: {os.getenv('DB_NAME')}")
        print(f"  User: {os.getenv('DB_USER')}")

if __name__ == '__main__':
    view_neon_data()
