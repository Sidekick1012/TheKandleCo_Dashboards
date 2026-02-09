import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv
import re
from datetime import datetime, timedelta

load_dotenv()

def get_db_connection():
    return psycopg2.connect( host=os.getenv('DB_HOST'), port=os.getenv('DB_PORT'), database=os.getenv('DB_NAME'), user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'))

def clean_val(val):
    if pd.isna(val) or val == '-' or val == '': return 0
    if isinstance(val, str):
        val = val.replace(',', '').replace('(', '-').replace(')', '').strip()
        if not val: return 0
        try: return float(val)
        except: return 0
    return float(val)

def extract_month_year(val):
    if pd.isna(val): return None
    match = re.search(r'([A-Za-z]+-\d{4})', str(val))
    return match.group(1) if match else None

def increment_month(month_str):
    # e.g. "Aug-2024" -> "Sep-2024"
    dt = datetime.strptime(month_str, "%b-%Y")
    next_dt = (dt.replace(day=28) + timedelta(days=4)).replace(day=1)
    return next_dt.strftime("%b-%Y")

def import_excel_to_db():
    xl_file = 'The Kandle Co. Notes Working 2024-2025.xlsx'
    print(f"Reading {xl_file}...")
    df_notes = pd.read_excel(xl_file, sheet_name='Notes', header=None)
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    tables_to_clear = ['profit_loss_summary', 'commission_details', 'stockist_sales_detail', 'custom_orders', 'salary_details', 'advertising_breakdown', 'administrative_expenses', 'cost_of_sales', 'sales_master', 'cash_bank_balances', 'accounts_payable', 'accounts_receivable', 'loans']
    print("Clearing existing data...")
    for t in tables_to_clear: cur.execute(f"TRUNCATE TABLE {t} CASCADE")
    
    monthly_data = {
        "Jul-2024": {
            'sales': {'online': 0, 'stockist': 0, 'custom': 0, 'exhibition': 0, 'details': []},
            'cash': {'hand': 0, 'bank': 0},
            'cos': {'cogs': 0, 'shopify': 0, 'commission': 0, 'freight': 0, 'fee': 0, 'comm_details': []},
            'admin': {'wages': 0, 'accounting': 0, 'postage': 0, 'advertising': 0, 'rent_off': 0, 'rent_ki': 0, 'internet': 0, 'electricity': 0, 'fuel': 0, 'packing': 0, 'salary_details': [], 'adv_details': []},
            'custom_orders': [], 'payable': [], 'receivable': [], 'loans': []
        }
    }
    current_month = "Jul-2024"
    last_detected_month = "Jul-2024"
    current_section = None
    
    print("Parsing Notes sheet...")
    for idx, row in df_notes.iterrows():
        # Flex Month Header Detection
        m = extract_month_year(row[9])
        is_new_month = False
        
        # Check if it's a generic "2024" or "2025" header that indicates a new month report
        val9 = str(row[9]).upper()
        if ("2024" in val9 or "2025" in val9) and ("RUPEES" in val9):
            if m: 
                # Standardize m to 3-letter if possible
                try:
                    dt_m = datetime.strptime(m, "%B-%Y") if len(m.split('-')[0]) > 3 else datetime.strptime(m, "%b-%Y")
                    m = dt_m.strftime("%b-%Y")
                except: pass
                current_month = m
                last_detected_month = m
            else:
                if idx > 1:
                    current_month = increment_month(last_detected_month)
                    last_detected_month = current_month
            
            is_new_month = True
            
        if is_new_month:
            if current_month not in monthly_data:
                monthly_data[current_month] = {
                    'sales': {'online': 0, 'stockist': 0, 'custom': 0, 'exhibition': 0, 'details': []},
                    'cash': {'hand': 0, 'bank': 0},
                    'cos': {'cogs': 0, 'shopify': 0, 'commission': 0, 'freight': 0, 'fee': 0, 'comm_details': []},
                    'admin': {'wages': 0, 'accounting': 0, 'postage': 0, 'advertising': 0, 'rent_off': 0, 'rent_ki': 0, 'internet': 0, 'electricity': 0, 'fuel': 0, 'packing': 0, 'salary_details': [], 'adv_details': []},
                    'custom_orders': [], 'payable': [], 'receivable': [], 'loans': []
                }
            current_section = None
            continue
            
        if not current_month: continue
        data = monthly_data[current_month]
        
        c1 = str(row[1]).strip() if not pd.isna(row[1]) else ""
        c2 = str(row[2]).strip() if not pd.isna(row[2]) else ""
        c3 = str(row[3]).strip() if not pd.isna(row[3]) else ""
        c5 = str(row[5]).strip() if not pd.isna(row[5]) else ""
        v5 = clean_val(row[5])
        v7 = clean_val(row[7])
        v9 = clean_val(row[9])
        
        # Section Detection
        is_header = False
        if c1 in ['1.1', '1.2', '1.3', '2.0', '2.1', '3.0', '3.2', '4.0', '4.1', '4.3', '5.0']:
            is_header = True
            if c1 == '1.1': current_section = 'SALES_STOCKIST'
            elif c1 == '1.2': current_section = 'SALES_CUSTOM'
            elif c1 == '1.3': current_section = 'SALES_EXHIBITION'
            elif c1 == '2.0': current_section = 'COS_COGS'
            elif c1 == '2.1': current_section = 'COS_COMMISSION'
            elif c1 == '3.0': current_section = 'ADMIN_WAGES'
            elif c1 == '3.2': current_section = 'ADMIN_ADV'
            elif c1 == '4.0': current_section = 'PAYABLE'
            elif c1 in ['4.1', '4.3']: current_section = 'LOAN'
            elif c1 == '5.0': current_section = 'RECEIVABLE'
        elif not c1 and c2:
            upp_c2 = c2.upper()
            if 'ONLINE SALES' in upp_c2: current_section = 'SALES_ONLINE'; is_header = True
            elif 'CASH IN HAND' in upp_c2: current_section = 'CASH_HAND'; is_header = True
            elif 'CASH AT BANK' in upp_c2 or 'CASH AT BANK' in c3.upper(): current_section = 'CASH_BANK'; is_header = True
            elif 'ADVERTISING & PROMOTIONS' in upp_c2: current_section = 'ADMIN_ADV'; is_header = True
            elif 'WAGES & SALARIES' in upp_c2: current_section = 'ADMIN_WAGES'; is_header = True
            elif 'ACCOUNTING & LEGAL' in upp_c2: current_section = 'ADMIN_ACC'; is_header = True
            elif 'POSTAGE & SHIPPING' in upp_c2: current_section = 'ADMIN_POST'; is_header = True
            elif 'RENT' in upp_c2 and ('OFFICE' in upp_c2 or 'KIOSK' in upp_c2 or 'TOTAL' not in upp_c2): current_section = 'ADMIN_RENT'; is_header = True
            elif 'COGS' in upp_c2: current_section = 'COS_COGS'; is_header = True

        label = c2 or c3 or (c5 if not isinstance(row[5], (int, float)) else "")
        amount = v5 or v9
        
        if is_header:
            if current_section == 'SALES_ONLINE': data['sales']['online'] = amount
            elif current_section == 'SALES_STOCKIST': data['sales']['stockist'] = amount
            elif current_section == 'SALES_CUSTOM': data['sales']['custom'] = amount
            elif current_section == 'CASH_HAND': data['cash']['hand'] = amount
            elif current_section == 'CASH_BANK': data['cash']['bank'] += amount
            elif current_section == 'COS_COGS': data['cos']['cogs'] = amount
            elif current_section == 'COS_COMMISSION': data['cos']['commission'] = amount
            elif current_section == 'ADMIN_WAGES': data['admin']['wages'] = amount
            elif current_section == 'ADMIN_ADV': data['admin']['advertising'] = amount
            elif current_section == 'ADMIN_ACC': data['admin']['accounting'] = amount
            elif current_section == 'ADMIN_POST': data['admin']['postage'] = amount
            if 'RENT' in c2.upper() and 'TOTAL' not in c2.upper(): 
                if 'OFFICE' in c2.upper(): data['admin']['rent_off'] = amount
                elif 'KIOSK' in c2.upper(): data['admin']['rent_ki'] = amount
        else:
            if current_section == 'SALES_STOCKIST' and amount > 0:
                data['sales']['details'].append({'name': label, 'amount': amount, 'pct': v7})
            elif current_section == 'SALES_CUSTOM' and amount > 0:
                data['custom_orders'].append({'name': label, 'amount': amount})
            elif current_section == 'COS_COMMISSION' and amount > 0:
                data['cos']['comm_details'].append({'name': label, 'amount': amount, 'pct': v7})
            elif current_section == 'ADMIN_WAGES' and amount > 0:
                data['admin']['salary_details'].append({'name': label, 'amount': amount})
            elif current_section == 'ADMIN_ADV' and amount > 0:
                data['admin']['adv_details'].append({'name': label, 'amount': amount})
            elif current_section == 'PAYABLE' and amount > 0:
                data['payable'].append({'name': label, 'amount': amount, 'pct': v7})
            elif current_section == 'RECEIVABLE' and amount > 0:
                data['receivable'].append({'name': label, 'amount': amount, 'pct': v7})
            elif current_section == 'LOAN' and amount > 0:
                data['loans'].append({'name': label, 'amount': amount})

        upp_l = label.upper()
        if 'SHOPIFY' in upp_l: data['cos']['shopify'] = amount
        elif 'FREIGHT' in upp_l: data['cos']['freight'] = amount
        elif 'SUBSCRIPTION' in upp_l: data['cos']['fee'] = amount
        elif 'INTERNET' in upp_l: data['admin']['internet'] = amount
        elif 'ELECTRICITY' in upp_l: data['admin']['electricity'] = amount
        elif 'FUEL' in upp_l: data['admin']['fuel'] = amount
        elif 'PACKING' in upp_l: data['admin']['packing'] = amount

    print(f"Inserting data for {len(monthly_data)} months...")
    for month, data in monthly_data.items():
        total_sa = data['sales']['online'] + data['sales']['stockist'] + data['sales']['custom'] + data['sales']['exhibition']
        cur.execute("INSERT INTO sales_master (month_year, online_sales, stockist_sales, custom_order_sales, exhibition_sales, total_sales) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id", (month, data['sales']['online'], data['sales']['stockist'], data['sales']['custom'], data['sales']['exhibition'], total_sa))
        sales_id = cur.fetchone()[0]
        for sd in data['sales']['details']: cur.execute("INSERT INTO stockist_sales_detail (sales_master_id, month_year, stockist_name, sales_amount, percentage) VALUES (%s, %s, %s, %s, %s)", (sales_id, month, sd['name'], sd['amount'], sd['pct']))
        for co in data['custom_orders']: cur.execute("INSERT INTO custom_orders (sales_master_id, month_year, customer_name, order_amount) VALUES (%s, %s, %s, %s)", (sales_id, month, co['name'], co['amount']))
        cur.execute("INSERT INTO cash_bank_balances (month_year, cash_in_hand, cash_at_bank, net_cash) VALUES (%s, %s, %s, %s)", (month, data['cash']['hand'], data['cash']['bank'], data['cash']['hand'] + data['cash']['bank']))
        total_cos = data['cos']['cogs'] + data['cos']['shopify'] + data['cos']['commission'] + data['cos']['freight'] + data['cos']['fee']
        cur.execute("INSERT INTO cost_of_sales (sales_master_id, month_year, cogs, shopify_fee, commission_expense, freight_cost, fee_subscription, total_cos) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id", (sales_id, month, data['cos']['cogs'], data['cos']['shopify'], data['cos']['commission'], data['cos']['freight'], data['cos']['fee'], total_cos))
        cos_id = cur.fetchone()[0]
        for cd in data['cos']['comm_details']: cur.execute("INSERT INTO commission_details (cost_of_sales_id, month_year, stockist_name, commission_amount, percentage) VALUES (%s, %s, %s, %s, %s)", (cos_id, month, cd['name'], cd['amount'], cd['pct']))
        total_ad = data['admin']['wages'] + data['admin']['accounting'] + data['admin']['postage'] + data['admin']['advertising'] + data['admin']['rent_off'] + data['admin']['rent_ki'] + data['admin']['internet'] + data['admin']['electricity'] + data['admin']['fuel'] + data['admin']['packing']
        cur.execute("INSERT INTO administrative_expenses (sales_master_id, month_year, wages_salaries, accounting_legal, postage_shipping, advertising_promotions, rent_office, rent_kiosk, internet, electricity, fuel_expense, packing_material, total_admin_expenses) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id", (sales_id, month, data['admin']['wages'], data['admin']['accounting'], data['admin']['postage'], data['admin']['advertising'], data['admin']['rent_off'], data['admin']['rent_ki'], data['admin']['internet'], data['admin']['electricity'], data['admin']['fuel'], data['admin']['packing'], total_ad))
        admin_id = cur.fetchone()[0]
        for sal in data['admin']['salary_details']: cur.execute("INSERT INTO salary_details (admin_expense_id, month_year, employee_name, salary_amount) VALUES (%s, %s, %s, %s)", (admin_id, month, sal['name'], sal['amount']))
        for adv in data['admin']['adv_details']:
            g, f, m_a = 0, 0, 0
            name = adv['name'].upper()
            if 'GOOGLE' in name: g = adv['amount']
            elif 'FACEBOOK' in name or 'META' in name: f = adv['amount']
            elif 'MARKETING' in name or 'AGENCY' in name: m_a = adv['amount']
            else: g = adv['amount']
            cur.execute("INSERT INTO advertising_breakdown (admin_expense_id, month_year, google_ads, facebook_ads, marketing_agency, total_advertising) VALUES (%s, %s, %s, %s, %s, %s)", (admin_id, month, g, f, m_a, adv['amount']))
        for p in data['payable']: cur.execute("INSERT INTO accounts_payable (month_year, supplier_name, amount_payable, percentage) VALUES (%s, %s, %s, %s)", (month, p['name'], p['amount'], p['pct']))
        for r in data['receivable']: cur.execute("INSERT INTO accounts_receivable (month_year, customer_name, amount_receivable, percentage) VALUES (%s, %s, %s, %s)", (month, r['name'], r['amount'], r['pct']))
        for l in data['loans']: cur.execute("INSERT INTO loans (month_year, loan_source, outstanding_amount) VALUES (%s, %s, %s)", (month, l['name'], l['amount']))
        gross = total_sa - data['cos']['cogs']
        cur.execute("INSERT INTO profit_loss_summary (sales_master_id, month_year, total_sales, total_cogs, gross_profit, gross_margin_percentage, total_admin_expenses, net_profit_loss, net_margin_percentage) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (sales_id, month, total_sa, data['cos']['cogs'], gross, (gross/total_sa*100 if total_sa>0 else 0), total_ad, gross - total_ad - (total_cos-data['cos']['cogs']), (gross - total_ad - (total_cos-data['cos']['cogs']))/total_sa*100 if total_sa>0 else 0))

    conn.commit()
    cur.close(); conn.close()
    print(f"Full Import for {len(monthly_data)} months completed successfully!")

if __name__ == '__main__': import_excel_to_db()
