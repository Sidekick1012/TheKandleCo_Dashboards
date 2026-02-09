"""
Simple script to check PostgreSQL connection and create users table
Run this after setting up your .env file with database credentials
"""

import psycopg2
import os
import sys
from dotenv import load_dotenv

# Fix encoding for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Load environment variables
load_dotenv()

def check_and_setup_database():
    """Check PostgreSQL connection and setup users table"""
    
    # Get credentials from .env
    db_config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '5432'),
        'database': os.getenv('DB_NAME', 'kandle_db'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', '')
    }
    
    print("[*] Checking PostgreSQL connection...")
    print(f"Host: {db_config['host']}")
    print(f"Database: {db_config['database']}")
    print(f"User: {db_config['user']}")
    print("-" * 50)
    
    try:
        # Try to connect
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        print("[+] Connection successful!")
        
        # Check if users table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'users'
            );
        """)
        table_exists = cursor.fetchone()[0]
        
        if table_exists:
            print("[+] Users table already exists!")
            
            # Check how many users exist
            cursor.execute("SELECT COUNT(*) FROM users;")
            user_count = cursor.fetchone()[0]
            print(f"[i] Total users: {user_count}")
            
            # Show usernames (not passwords!)
            cursor.execute("SELECT username, created_at FROM users ORDER BY created_at;")
            users = cursor.fetchall()
            print("\n[i] Users in database:")
            for username, created_at in users:
                print(f"   - {username} (created: {created_at})")
            
        else:
            print("[!] Users table does not exist. Creating now...")
            
            # Create users table
            cursor.execute('''
                CREATE TABLE users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(255) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create index
            cursor.execute('CREATE INDEX idx_username ON users(username);')
            
            # Add default admin user
            import hashlib
            default_password = hashlib.sha256("kandle2024".encode()).hexdigest()
            cursor.execute(
                'INSERT INTO users (username, password_hash) VALUES (%s, %s)',
                ('admin', default_password)
            )
            
            conn.commit()
            print("[+] Users table created successfully!")
            print("[+] Default admin user created (admin / kandle2024)")
        
        cursor.close()
        conn.close()
        print("\n[+] Database is ready!")
        
    except psycopg2.OperationalError as e:
        print("[-] Connection failed!")
        print(f"Error: {e}")
        print("\n[!] Make sure:")
        print("1. PostgreSQL is running")
        print("2. .env file has correct credentials")
        print("3. Database exists (create it if not)")
        
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    print("="*50)
    print("PostgreSQL Database Checker")
    print("="*50)
    check_and_setup_database()
