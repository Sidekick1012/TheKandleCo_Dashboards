"""
Generate Excel Template for Monthly Data Entry
This creates a blank template with all required tables
"""

import pandas as pd
from datetime import datetime

# Create Excel writer
output_file = "Monthly_Data_Template.xlsx"

with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    
    # 1. SALES MASTER
    sales_master = pd.DataFrame({
        'month': ['Jul-2025'],
        'total_sales': [0.00],
        'cash_position': [1.00]
    })
    sales_master.to_excel(writer, sheet_name='sales_master', index=False)
    
    # 2. PROFIT LOSS SUMMARY
    profit_loss = pd.DataFrame({
        'month': ['Jul-2025'],
        'revenue': [0.00],
        'cogs': [0.00],
        'gross_profit': [0.00],
        'gross_margin': [0.00],
        'admin_expenses': [0.00],
        'advertising': [0.00],
        'net_profit': [0.00],
        'net_margin': [0.00]
    })
    profit_loss.to_excel(writer, sheet_name='profit_loss_summary', index=False)
    
    # 3. STOCKIST SALES DETAIL
    stockist_sales = pd.DataFrame({
        'month_id': [44, 44, 44],
        'month': ['Jul-2025', 'Jul-2025', 'Jul-2025'],
        'channel': ['Sales Shams', 'Alfateh-CRST Store', 'Sales Kayal'],
        'amount': [0.00, 0.00, 0.00],
        'percentage': [0.00, 0.00, 0.00]
    })
    stockist_sales.to_excel(writer, sheet_name='stockist_sales_detail', index=False)
    
    # 4. COMMISSION DETAILS
    commission = pd.DataFrame({
        'month': ['Jul-2025', 'Jul-2025'],
        'stockist': ['Sales Shams', 'Alfateh-CRST Store'],
        'amount': [0.00, 0.00]
    })
    commission.to_excel(writer, sheet_name='commission_details', index=False)
    
    # 5. ADMINISTRATIVE EXPENSES
    admin_expenses = pd.DataFrame({
        'month': ['Jul-2025'],
        'rent': [0.00],
        'utilities': [0.00],
        'salaries': [0.00],
        'other': [0.00],
        'total': [0.00]
    })
    admin_expenses.to_excel(writer, sheet_name='administrative_expenses', index=False)
    
    # 6. ADVERTISING BREAKDOWN
    advertising = pd.DataFrame({
        'month': ['Jul-2025', 'Jul-2025', 'Jul-2025'],
        'platform': ['Social Media', 'Google Ads', 'Print Media'],
        'amount': [0.00, 0.00, 0.00]
    })
    advertising.to_excel(writer, sheet_name='advertising_breakdown', index=False)
    
    # 7. SALARY DETAILS
    salary = pd.DataFrame({
        'month': ['Jul-2025', 'Jul-2025'],
        'employee': ['Manager', 'Sales Staff'],
        'salary': [0.00, 0.00]
    })
    salary.to_excel(writer, sheet_name='salary_details', index=False)
    
    # 8. ACCOUNTS PAYABLE
    accounts_payable = pd.DataFrame({
        'month': ['Jul-2025'],
        'vendor': ['Supplier 1'],
        'amount': [0.00],
        'due_date': [datetime.now().date()]
    })
    accounts_payable.to_excel(writer, sheet_name='accounts_payable', index=False)
    
    # 9. ACCOUNTS RECEIVABLE
    accounts_receivable = pd.DataFrame({
        'month': ['Jul-2025'],
        'customer': ['Customer 1'],
        'amount': [0.00],
        'due_date': [datetime.now().date()]
    })
    accounts_receivable.to_excel(writer, sheet_name='accounts_receivable', index=False)
    
    # 10. CUSTOM ORDERS
    custom_orders = pd.DataFrame({
        'month': ['Jul-2025'],
        'order_id': ['ORD001'],
        'customer': ['Customer Name'],
        'amount': [0.00],
        'status': ['Pending']
    })
    custom_orders.to_excel(writer, sheet_name='custom_orders', index=False)
    
    # 11. CASH BANK BALANCES
    cash_bank = pd.DataFrame({
        'month': ['Jul-2025'],
        'cash': [0.00],
        'bank': [0.00],
        'total': [0.00]
    })
    cash_bank.to_excel(writer, sheet_name='cash_bank_balances', index=False)
    
    # 12. COST OF SALES
    cost_of_sales = pd.DataFrame({
        'month': ['Jul-2025'],
        'raw_materials': [0.00],
        'labor': [0.00],
        'overhead': [0.00],
        'total': [0.00]
    })
    cost_of_sales.to_excel(writer, sheet_name='cost_of_sales', index=False)
    
    # 13. LOANS
    loans = pd.DataFrame({
        'month': ['Jul-2025'],
        'loan_type': ['Bank Loan'],
        'amount': [0.00],
        'interest_rate': [0.00],
        'monthly_payment': [0.00]
    })
    loans.to_excel(writer, sheet_name='loans', index=False)

print(f"✅ Template created: {output_file}")
print("\n📋 Template includes 13 sheets:")
print("   1. sales_master")
print("   2. profit_loss_summary")
print("   3. stockist_sales_detail")
print("   4. commission_details")
print("   5. administrative_expenses")
print("   6. advertising_breakdown")
print("   7. salary_details")
print("   8. accounts_payable")
print("   9. accounts_receivable")
print("   10. custom_orders")
print("   11. cash_bank_balances")
print("   12. cost_of_sales")
print("   13. loans")
print("\n📝 Instructions:")
print("   - Replace 'Jul-2025' with your actual month")
print("   - Fill in your data in each sheet")
print("   - Keep column names EXACTLY as shown")
print("   - Use this file with import_data.py")
