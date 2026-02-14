import pandas as pd
import psycopg2
import os
import streamlit as st
import numpy as np
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# ================= MOCK DATA GENERATOR =================
class MockDataGenerator:
    def __init__(self):
        # Generate all months for 2024 and 2025
        self.months = []
        # Generate Jan-2024 to Dec-2025
        for year in [2024, 2025]:
            for month_idx in range(1, 13):
                date_obj = datetime(year, month_idx, 1)
                self.months.append(date_obj.strftime("%b-%Y"))
            
    def get_monthly_sales_trend(self):
        n = len(self.months)
        data = {
            "month_year": self.months,
            "online_sales": np.random.randint(500000, 1500000, n),
            "stockist_sales": np.random.randint(200000, 800000, n),
            "custom_order_sales": np.random.randint(100000, 500000, n),
            "exhibition_sales": np.random.randint(0, 300000, n)
        }
        df = pd.DataFrame(data)
        df['total_sales'] = df['online_sales'] + df['stockist_sales'] + df['custom_order_sales'] + df['exhibition_sales']
        return df

    def get_profit_loss_trends(self):
        df_sales = self.get_monthly_sales_trend()
        n = len(df_sales)
        df = df_sales[['month_year', 'total_sales']].copy()
        
        # Approximate COGS as 35-45% of sales
        df['total_cogs'] = (df['total_sales'] * np.random.uniform(0.35, 0.45, n)).astype(int)
        df['gross_profit'] = df['total_sales'] - df['total_cogs']
        df['gross_margin_percentage'] = (df['gross_profit'] / df['total_sales'] * 100).round(1)
        
        # Admin expenses approx 30-40% 
        df['total_admin_expenses'] = (df['total_sales'] * np.random.uniform(0.30, 0.40, n)).astype(int)
        df['net_profit_loss'] = df['gross_profit'] - df['total_admin_expenses']
        df['net_margin_percentage'] = (df['net_profit_loss'] / df['total_sales'] * 100).round(1)
        
        return df

    def get_stockist_performance(self, month=None):
        stockists = ["Luxe Living", "Home & Hearth", "The Gift Shop", "Urban Decor", "Pure Home", "Style Studio"]
        data = []
        
        if month:
            for s in stockists:
                sales = np.random.randint(50000, 200000)
                comm_pct = 20
                data.append({
                    "stockist_name": s,
                    "sales_amount": sales,
                    "percentage": comm_pct,
                    "month_year": month
                })
        else:
            # Generate for ALL months to allow filtering later
            for m in self.months:
                for s in stockists:
                    sales = np.random.randint(5000, 50000) # smaller per month
                    data.append({
                        "stockist_name": s,
                        "sales_amount": sales,
                        "month_year": m
                    })
        return pd.DataFrame(data)

    def get_commission_data(self):
        stockists = ["Luxe Living", "Home & Hearth", "The Gift Shop", "Urban Decor", "Pure Home", "Style Studio"]
        data = []
        for s in stockists:
            comm = np.random.randint(100000, 400000)
            data.append({"stockist_name": s, "total_comm": comm})
        return pd.DataFrame(data)

    def get_expense_breakdown(self, month=None):
        n = len(self.months)
        data = {
            "month_year": self.months,
            "wages_salaries": np.random.randint(200000, 300000, n),
            "rent_office": [80000] * n,
            "rent_kiosk": [50000] * n,
            "advertising_promotions": np.random.randint(50000, 150000, n),
            "electricity": np.random.randint(20000, 40000, n),
            "fuel_expense": np.random.randint(10000, 25000, n),
            "internet": [5000] * n
        }
        df = pd.DataFrame(data)
        df['total_admin_expenses'] = df.drop('month_year', axis=1).sum(axis=1)
        
        if month:
            return df[df['month_year'] == month]
        return df

    def get_cash_flow_data(self):
        n = len(self.months)
        data = {
            "month_year": self.months,
            "cash_in_hand": np.random.randint(20000, 100000, n),
            "cash_at_bank": np.random.randint(500000, 2000000, n)
        }
        df = pd.DataFrame(data)
        df['net_cash'] = df['cash_in_hand'] + df['cash_at_bank']
        return df

    def get_marketing_spend(self):
        n = len(self.months)
        data = {
            "month_year": self.months,
            "google_ads": np.random.randint(20000, 50000, n),
            "facebook_ads": np.random.randint(30000, 80000, n),
            "marketing_agency": [50000] * n
        }
        df = pd.DataFrame(data)
        df['total_advertising'] = df['google_ads'] + df['facebook_ads'] + df['marketing_agency']
        return df

    def get_payroll_data(self):
        employees = ["Ahmed Khan", "Sara Ali", "Bilal Ahmed", "Fatima Noor", "Zainab Bibi"]
        data = []
        for m in self.months:
            for e in employees:
                data.append({
                    "month_year": m,
                    "employee_name": e,
                    "salary_amount": np.random.randint(40000, 80000)
                })
        return pd.DataFrame(data)

    def get_receivables_payables(self):
        n = len(self.months)
        # Payables
        p_data = {
            "month_year": self.months,
            "total_payable": np.random.randint(100000, 500000, n)
        }
        # Receivables
        r_data = {
            "month_year": self.months,
            "total_receivable": np.random.randint(150000, 600000, n)
        }
        return pd.DataFrame(p_data), pd.DataFrame(r_data)

    def get_custom_orders(self):
        customers = ["Hotel One", "Serena", "Corporate Gift Co", "Wedding Planner A", "Cafe X"]
        data = []
        for c in customers:
            data.append({
                "customer_name": c,
                "total_rev": np.random.randint(100000, 500000),
                "order_amount": np.random.randint(50000, 200000)
            })
        return pd.DataFrame(data)

    def get_payables_detail(self):
        suppliers = ["Wax Co", "Fragrance World", "Glass Hub", "Packaging Pro", "Wick Masters"]
        data = []
        for s in suppliers:
            data.append({
                "supplier_name": s,
                "total_p": np.random.randint(50000, 200000),
                "amount_payable": np.random.randint(10000, 50000)
            })
        return pd.DataFrame(data)

    def get_receivables_detail(self):
        customers = ["Luxe Living", "Home & Hearth", "Hotel One", "Serena"]
        data = []
        for c in customers:
            data.append({
                "customer_name": c,
                "amount_receivable": np.random.randint(20000, 100000),
                "percentage": np.random.randint(5, 30)
            })
        return pd.DataFrame(data)

    def get_all_customers(self):
        """Mock data for all customers directory"""
        customers = ["Hotel One", "Serena", "Corporate Gift Co", "Wedding Planner A", "Cafe X", 
                    "Pearl Continental", "Marriott Hotel", "Elite Events", "Grand Banquet"]
        data = []
        for c in customers:
            data.append({
                "customer_name": c,
                "total_revenue": np.random.randint(200000, 800000),
                "total_orders": np.random.randint(100000, 400000),
                "order_count": np.random.randint(3, 15)
            })
        return pd.DataFrame(data)
    
    def get_all_stockists(self):
        """Mock data for all stockists directory"""
        stockists = ["Luxe Living", "Home & Hearth", "The Gift Shop", "Urban Decor", 
                    "Pure Home", "Style Studio", "Decor Zone", "Lifestyle Boutique"]
        data = []
        for s in stockists:
            data.append({
                "stockist_name": s,
                "total_sales": np.random.randint(500000, 2000000),
                "active_months": np.random.randint(6, 24)
            })
        return pd.DataFrame(data)

    def get_all_products(self):
        """Real product catalog from 2024-2025 Working Notes"""
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
        return pd.DataFrame(products)



# ================= DB CONNECTION =================
mock_gen = MockDataGenerator()

def get_db_connection():
    try:
        # 1. Try Environment Variables (Prioritize Local Dev with .env)
        if os.getenv('DB_HOST'):
            conn = psycopg2.connect(
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT', '5432'),
                database=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                connect_timeout=3
            )
            return conn

        # 2. Fallback to Streamlit Secrets (Cloud Deployment)
        if hasattr(st, "secrets") and "DB_HOST" in st.secrets:
            conn = psycopg2.connect(
                host=st.secrets["DB_HOST"],
                port=str(st.secrets.get("DB_PORT", "5432")),
                database=st.secrets["DB_NAME"],
                user=st.secrets["DB_USER"],
                password=st.secrets["DB_PASSWORD"],
                connect_timeout=3
            )
            return conn
            
        return None
    except Exception as e:
        print(f"❌ DB Connection Error in data_utils: {e}")
        return None

def fetch_data(query, params=None):
    conn = get_db_connection()
    if conn:
        try:
            df = pd.read_sql_query(query, conn, params=params)
            return df
        except Exception as e:
            pass # Fallback to mock
        finally:
            if conn: conn.close()
    
    # --- MOCK FALLBACKS ---
    q_lower = query.lower()
    
    if "sales_master" in q_lower:
        return mock_gen.get_monthly_sales_trend()
    elif "profit_loss_summary" in q_lower:
        return mock_gen.get_profit_loss_trends()
    elif "stockist_sales_detail" in q_lower:
        # Check if it's the aggregated stockist directory query
        if "sum(sales_amount)" in q_lower and "group by stockist_name" in q_lower:
            return mock_gen.get_all_stockists()
        return mock_gen.get_stockist_performance()
    elif "commission_details" in q_lower:
        return mock_gen.get_commission_data()
    elif "administrative_expenses" in q_lower:
        return mock_gen.get_expense_breakdown()
    elif "cash_bank_balances" in q_lower:
        return mock_gen.get_cash_flow_data()
    elif "advertising_breakdown" in q_lower:
        return mock_gen.get_marketing_spend()
    elif "salary_details" in q_lower:
        return mock_gen.get_payroll_data()
    elif "accounts_payable" in q_lower:
        if "group by" in q_lower:
            p, _ = mock_gen.get_receivables_payables()
            return p
        return mock_gen.get_payables_detail()
    elif "accounts_receivable" in q_lower:
        if "group by" in q_lower:
            _, r = mock_gen.get_receivables_payables()
            return r
        return mock_gen.get_receivables_detail()
    elif "custom_orders" in q_lower:
        # Check if it's the aggregated customer directory query
        if "sum(total_rev)" in q_lower and "group by customer_name" in q_lower:
            return mock_gen.get_all_customers()
        return mock_gen.get_custom_orders()
    elif "count(distinct stockist_name)" in q_lower:
        return pd.DataFrame([{"count": 6}])
    
    return pd.DataFrame()

# ================= WRAPPER FUNCTIONS =================

def apply_filters(df, year=None, months=None):
    """Utility to filter dataframe by year and months based on month_year column"""
    if df.empty or 'month_year' not in df.columns:
        return df
    
    # Standardize selected year/months
    if year is None: year = 2025
    if months is None: months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Create copy to avoid SettingWithCopyWarning
    df = df.copy()
    
    # Extract year and month from 'Mon-YYYY' format
    df[['m_str', 'y_str']] = df['month_year'].str.split('-', expand=True)
    
    # Filter
    mask = (df['y_str'] == str(year)) & (df['m_str'].isin(months))
    df = df[mask].drop(['m_str', 'y_str'], axis=1)
    
    return df

def get_monthly_sales_trend():
    query = "SELECT month_year, online_sales, stockist_sales, custom_order_sales, exhibition_sales, total_sales FROM sales_master"
    return fetch_data(query)

def get_profit_loss_trends():
    query = "SELECT month_year, total_sales, total_cogs, gross_profit, gross_margin_percentage, total_admin_expenses, net_profit_loss, net_margin_percentage FROM profit_loss_summary"
    return fetch_data(query)

def get_stockist_performance():
    query = "SELECT stockist_name, sales_amount, month_year FROM stockist_sales_detail"
    return fetch_data(query)

def get_expense_breakdown():
    query = "SELECT * FROM administrative_expenses"
    return fetch_data(query)

def get_cash_flow_data():
    query = "SELECT month_year, cash_in_hand, cash_at_bank, net_cash FROM cash_bank_balances"
    return fetch_data(query)

def get_marketing_spend():
    query = "SELECT month_year, google_ads, facebook_ads, marketing_agency, total_advertising FROM advertising_breakdown"
    return fetch_data(query)

def get_payroll_data():
    query = "SELECT month_year, employee_name, salary_amount FROM salary_details"
    return fetch_data(query)

def get_receivables_payables():
    pay_query = "SELECT month_year, SUM(amount_payable) as total_payable FROM accounts_payable GROUP BY month_year"
    rec_query = "SELECT month_year, SUM(amount_receivable) as total_receivable FROM accounts_receivable GROUP BY month_year"
    return fetch_data(pay_query), fetch_data(rec_query)

def get_custom_orders():
    query = "SELECT customer_name, total_rev, order_amount FROM custom_orders"
    return fetch_data(query)

def get_payables_detail():
    query = "SELECT supplier_name, amount_payable as total_p FROM accounts_payable" # Mocked field name diff
    return fetch_data(query)

def get_receivables_detail():
    query = "SELECT customer_name, amount_receivable, percentage FROM accounts_receivable"
    return fetch_data(query)

def get_yoy_growth_data():
    df = get_monthly_sales_trend()
    if df.empty: return pd.DataFrame()
    
    df = df.copy()
    df[['month_name', 'year']] = df['month_year'].str.split('-', expand=True)
    
    # Filter out rows where year is None or empty
    df = df[df['year'].notna() & (df['year'] != '')]
    
    if df.empty: return pd.DataFrame()
    
    # Pivot
    df_pivot = df.pivot_table(index='month_name', columns='year', values='total_sales', aggfunc='sum')
    
    months_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    df_pivot = df_pivot.reindex(months_order)
    return df_pivot

def get_top_stockists():
    df = get_stockist_performance()
    if df.empty: return pd.DataFrame()
    return df.groupby('stockist_name')['sales_amount'].sum().reset_index().sort_values('sales_amount', ascending=False)

def get_alerts(year=2025, months=None):
    if months is None: months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    alerts = []
    
    df_pl = apply_filters(get_profit_loss_trends(), year, months)
    if not df_pl.empty and len(df_pl) >= 1:
        avg_gross = df_pl['gross_margin_percentage'].mean()
        if avg_gross < 55:
            alerts.append({"type": "warning", "message": f"Average Gross Margin for selected period is low ({avg_gross:.1f}%). Target: 60%"})
            
    df_cash = apply_filters(get_cash_flow_data(), year, months)
    if not df_cash.empty:
        curr_cash = df_cash.iloc[-1]['net_cash']
        if curr_cash < 1000000:
             alerts.append({"type": "danger", "message": f"Cash Position at end of period is critical (Rs. {curr_cash:,.0f})."})
             
    # Seasonal reminders
    if 'Oct' in months or 'Nov' in months:
        alerts.append({"type": "info", "message": "Peak season (Diwali/Holiday) detected in selection. Ensure stock levels are high."})
        
    return alerts

def get_unit_economics_data(year=2025, months=None):
    """
    Enhanced version of profitability proxy for the 'Margin Doctor' dashboard.
    Calculates SKU-level margins and estimates volumes based on filters.
    """
    df_products = get_all_products()
    if df_products.empty:
        return pd.DataFrame()
        
    products_data = []
    
    # Calculate Overhead (Marketing + Packaging) for the selected period
    df_exp_all = get_expense_breakdown()
    df_exp = apply_filters(df_exp_all, year, months)
    
    if not df_exp.empty:
        # Total for selection
        total_marketing = df_exp['advertising_promotions'].sum()
        total_packing = df_exp['packing_material'].sum()
    else:
        # Fallbacks for empty selection (pro-rated)
        n_m = len(months) if months else 12
        total_marketing, total_packing = 50000 * n_m, 20000 * n_m
        
    # Estimate total units sold in the selected period
    # Assume 1200 units/avg month
    n_months = len(months) if months else 12
    total_est_units = 1200 * n_months
    
    mkt_per_unit = total_marketing / total_est_units if total_est_units > 0 else 0
    pack_per_unit = total_packing / total_est_units if total_est_units > 0 else 0
    
    for _, row in df_products.iterrows():
        cost = row['cost']
        price = row['price']
        
        # Gross Margin (Price - Material Cost)
        gross_profit = price - cost
        margin_pct = (gross_profit / price) * 100
        
        # Simulate Volume (Historical trend proxy)
        # Some are popular (Winners), some are niche
        if "Oud" in row['name'] or "Lavender" in row['name']:
            vol_multiplier = 1.5
        elif "Vanilla" in row['name'] or "Cinnamon" in row['name']:
            vol_multiplier = 1.2
        else:
            vol_multiplier = 1.0
            
        base_vol = 800 if row['variant'] == '100g' else 300
        # Scale volume by number of months
        scaled_base = (base_vol * (n_months / 12)) * vol_multiplier
        volume = int(np.random.normal(scaled_base, scaled_base * 0.1 if scaled_base > 0 else 1))
        
        products_data.append({
            "SKU": row['sku'],
            "Product": f"{row['name']} ({row['variant']})",
            "Category": row['category'],
            "Sales Volume": volume,
            "Gross Margin %": round(margin_pct, 1),
            "Price": price,
            "Material Cost": cost,
            "Marketing per Unit": round(mkt_per_unit, 0),
            "Packing per Unit": round(pack_per_unit, 0),
            "Net Profit per Unit": round(gross_profit - mkt_per_unit - pack_per_unit, 0)
        })
        
    return pd.DataFrame(products_data)

def get_cost_per_unit_data(sku=None):
    """
    Returns the breakdown of costs for a specific SKU or a general average.
    """
    df_econ = get_unit_economics_data()
    if df_econ.empty:
        return pd.DataFrame()
        
    if sku:
        row = df_econ[df_econ['SKU'] == sku].iloc[0]
    else:
        # Pick a representative one (e.g. 100g Burning Firewood)
        row = df_econ.iloc[0]
        
    breakdown = [
        {"Component": "Raw Materials", "Cost": row['Material Cost']},
        {"Component": "Packaging", "Cost": row['Packing per Unit']},
        {"Component": "Marketing (Ad Spend)", "Cost": row['Marketing per Unit']},
        # Proxying Shipping at ~5% of price
        {"Component": "Shipping/Logistics", "Cost": round(row['Price'] * 0.05, 0)}
    ]
    return pd.DataFrame(breakdown)

def get_product_profitability_proxy():
    # Keep legacy for compatibility or wrap the new one
    return get_unit_economics_data().rename(columns={
        "Product": "name",
        "Gross Margin %": "margin",
        "Sales Volume": "volume"
    })

# ================= CUSTOMER & PRODUCT DIRECTORY FUNCTIONS =================

def get_all_customers():
    """Get all unique customers from custom orders with totals"""
    query = """
        SELECT 
            customer_name,
            SUM(order_amount) as total_revenue,
            COUNT(*) as order_count
        FROM custom_orders
        WHERE customer_name IS NOT NULL
        GROUP BY customer_name
        ORDER BY total_revenue DESC
    """
    return fetch_data(query)

def get_all_stockists():
    """Get all unique stockists/partners with performance metrics"""
    query = """
        SELECT 
            stockist_name,
            SUM(sales_amount) as total_sales,
            COUNT(DISTINCT month_year) as active_months
        FROM stockist_sales_detail
        WHERE stockist_name IS NOT NULL AND stockist_name != ''
        GROUP BY stockist_name
        ORDER BY total_sales DESC
    """
    return fetch_data(query)

def get_sales_channel_summary():
    """Get summary of all sales channels"""
    query = """
        SELECT 
            month_year,
            online_sales,
            stockist_sales,
            custom_order_sales,
            exhibition_sales,
            total_sales
        FROM sales_master
        ORDER BY month_year DESC
    """
    return fetch_data(query)

def get_all_products():
    """Get the full product catalog"""
    # 1. Try to fetch from Real Database
    query = "SELECT sku, name, variant, category, cost, price FROM products ORDER BY category, name"
    df = fetch_data(query)
    
    if not df.empty:
         return df
         
    # 2. Fallback to Mock if DB is empty or connection fails
    return mock_gen.get_all_products()


