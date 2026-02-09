import psycopg2
from psycopg2 import pool
import hashlib
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# PostgreSQL Configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'analytics_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', '')
}

# Connection pool for better performance
connection_pool = None

def init_connection_pool():
    """Initialize PostgreSQL connection pool"""
    global connection_pool
    try:
        connection_pool = psycopg2.pool.SimpleConnectionPool(
            1, 10,  # min and max connections
            **DB_CONFIG
        )
        if connection_pool:
            print("[+] PostgreSQL connection pool created successfully")
    except Exception as e:
        print(f"[-] Error creating connection pool: {e}")
        raise

def get_connection():
    """Get a connection from the pool"""
    if connection_pool is None:
        init_connection_pool()
    return connection_pool.getconn()

def release_connection(conn):
    """Release connection back to the pool"""
    if connection_pool:
        connection_pool.putconn(conn)

def init_db():
    """Initialize the database and create users table if it doesn't exist"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Create users table with PostgreSQL syntax
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create index on username for faster lookups
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_username ON users(username)
        ''')
        
        # Check if any users exist
        cursor.execute('SELECT COUNT(*) FROM users')
        count = cursor.fetchone()[0]
        
        if count == 0:
            # Create default admin user
            default_user = "admin"
            default_password = "admin2024"
            password_hash = hashlib.sha256(default_password.encode()).hexdigest()
            
            cursor.execute(
                'INSERT INTO users (username, password_hash) VALUES (%s, %s)',
                (default_user, password_hash)
            )
            conn.commit()
            print(f"[+] Default user created: {default_user} / {default_password}")
        else:
            print(f"[+] Database initialized with {count} user(s)")
        
        cursor.close()
        
    except Exception as e:
        print(f"[-] Database initialization error: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            release_connection(conn)

def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def check_login(username, password):
    """Verify user credentials"""
    if not username or not password:
        return False
    
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        password_hash = hash_password(password)
        
        cursor.execute(
            'SELECT id FROM users WHERE username = %s AND password_hash = %s',
            (username, password_hash)
        )
        
        result = cursor.fetchone()
        cursor.close()
        
        return result is not None
        
    except Exception as e:
        print(f"[-] Login error: {e}")
        return False
    finally:
        if conn:
            release_connection(conn)

def add_user(username, password):
    """Add a new user to the database"""
    if not username or not password:
        return False, "Username and password are required"
    
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        password_hash = hash_password(password)
        cursor.execute(
            'INSERT INTO users (username, password_hash) VALUES (%s, %s)',
            (username, password_hash)
        )
        
        conn.commit()
        cursor.close()
        return True, "User created successfully"
        
    except psycopg2.IntegrityError:
        if conn:
            conn.rollback()
        return False, "Username already exists"
    except Exception as e:
        if conn:
            conn.rollback()
        return False, f"Error: {str(e)}"
    finally:
        if conn:
            release_connection(conn)

def change_password(username, old_password, new_password):
    """Change user password"""
    if not check_login(username, old_password):
        return False, "Invalid current password"
    
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        new_password_hash = hash_password(new_password)
        cursor.execute(
            'UPDATE users SET password_hash = %s WHERE username = %s',
            (new_password_hash, username)
        )
        
        conn.commit()
        cursor.close()
        return True, "Password changed successfully"
        
    except Exception as e:
        if conn:
            conn.rollback()
        return False, f"Error: {str(e)}"
    finally:
        if conn:
            release_connection(conn)

def close_all_connections():
    """Close all connections in the pool (call on app shutdown)"""
    global connection_pool
    if connection_pool:
        connection_pool.closeall()
        print("[+] All database connections closed")