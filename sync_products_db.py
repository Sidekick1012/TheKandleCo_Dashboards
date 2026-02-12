import psycopg2
import os
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Cloud Database Config
DB_HOST = "ep-late-water-aiygvdom-pooler.c-4.us-east-1.aws.neon.tech"
DB_NAME = "neondb"
DB_USER = "neondb_owner"
DB_PASS = "npg_57zhogBbOGvA" # From migrate_to_cloud.py

def get_product_data():
    """Returns the list of products extracted from Excel"""
    # This data matches what we put in data_utils.py
    products = [
        # 100g Candles (Selling: 2000, Cost: ~732)
        {"sku": "7001", "name": "Burning Firewood", "variant": "100g", "category": "Candle", "cost": 732, "price": 2000},
        {"sku": "7003", "name": "Cinnamon Apple", "variant": "100g", "category": "Candle", "cost": 732, "price": 2000},
        {"sku": "7004", "name": "Citrus Bloom", "variant": "100g", "category": "Candle", "cost": 732, "price": 2000},
        {"sku": "7005", "name": "Double Shot Espresso", "variant": "100g", "category": "Candle", "cost": 732, "price": 2000},
        {"sku": "7006", "name": "Flower Bouquet", "variant": "100g", "category": "Candle", "cost": 732, "price": 2000},
        {"sku": "7007", "name": "Honeysuckle Jasmine", "variant": "100g", "category": "Candle", "cost": 732, "price": 2000},
        {"sku": "7008", "name": "Lavender Breeze", "variant": "100g", "category": "Candle", "cost": 732, "price": 2000},
        {"sku": "7011", "name": "Oud Fusion", "variant": "100g", "category": "Candle", "cost": 732, "price": 2000},
        {"sku": "7012", "name": "Pink Blossoms", "variant": "100g", "category": "Candle", "cost": 732, "price": 2000},
        {"sku": "7013", "name": "Rose & Sandalwood", "variant": "100g", "category": "Candle", "cost": 732, "price": 2000},
        {"sku": "7015", "name": "Toasted Vanilla", "variant": "100g", "category": "Candle", "cost": 732, "price": 2000},
        {"sku": "7016", "name": "Tropical Peach", "variant": "100g", "category": "Candle", "cost": 732, "price": 2000},
        {"sku": "7017", "name": "Watermelon Summer", "variant": "100g", "category": "Candle", "cost": 732, "price": 2000},
        {"sku": "7018", "name": "White Garden", "variant": "100g", "category": "Candle", "cost": 732, "price": 2000},
        
        # 250g Candles (Selling: 3800, Cost: ~1598)
        {"sku": "7020", "name": "Burning Firewood", "variant": "250g", "category": "Candle", "cost": 1598, "price": 3800},
        {"sku": "7022", "name": "Cinnamon Apple", "variant": "250g", "category": "Candle", "cost": 1598, "price": 3800},
        {"sku": "7023", "name": "Citrus Bloom", "variant": "250g", "category": "Candle", "cost": 1598, "price": 3800},
        {"sku": "7024", "name": "Double Shot Espresso", "variant": "250g", "category": "Candle", "cost": 1598, "price": 3800},
        {"sku": "7025", "name": "Flower Bouquet", "variant": "250g", "category": "Candle", "cost": 1598, "price": 3800},
        {"sku": "7026", "name": "Honeysuckle Jasmine", "variant": "250g", "category": "Candle", "cost": 1598, "price": 3800},
        {"sku": "7027", "name": "Lavender Breeze", "variant": "250g", "category": "Candle", "cost": 1598, "price": 3800},
        {"sku": "7030", "name": "Oud Fusion", "variant": "250g", "category": "Candle", "cost": 1598, "price": 3800},
        
        # Other Categories (Inferred)
        {"sku": "8001", "name": "Standard Diffuser", "variant": "100ml", "category": "Diffuser", "cost": 1200, "price": 2800},
        {"sku": "8002", "name": "Refill Pack", "variant": "100ml", "category": "Refill", "cost": 800, "price": 1800},
        {"sku": "8003", "name": "Room Spray", "variant": "100ml", "category": "Spray", "cost": 600, "price": 1500},
    ]
    return products

def sync_products():
    print("🚀 Connecting to Neon Database...")
    
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        cur = conn.cursor()
        print("✅ Connected!")
        
        # 1. Create Table
        print("📦 Creating 'products' table...")
        create_sql = """
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            sku VARCHAR(50),
            name VARCHAR(255),
            variant VARCHAR(50),
            category VARCHAR(50),
            cost NUMERIC,
            price NUMERIC,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cur.execute(create_sql)
        print("✅ Table created/verified.")
        
        # 2. Clear existing data
        print("🧹 Clearing existing product data...")
        cur.execute("TRUNCATE TABLE products RESTART IDENTITY;")
        
        # 3. Insert Data
        print("📝 Inserting real product data...")
        products = get_product_data()
        
        insert_sql = """
        INSERT INTO products (sku, name, variant, category, cost, price)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        count = 0
        for p in products:
            cur.execute(insert_sql, (
                p['sku'], p['name'], p['variant'], p['category'], p['cost'], p['price']
            ))
            count += 1
            
        conn.commit()
        print(f"✅ Successfully inserted {count} products!")
        
        # Verification
        cur.execute("SELECT COUNT(*) FROM products")
        final_count = cur.fetchone()[0]
        print(f"🕵️ Verification: Table now has {final_count} rows.")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    sync_products()
