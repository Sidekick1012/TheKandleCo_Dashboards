import streamlit as st
import time
import pandas as pd
import plotly.express as px
from login import init_db, check_login
from data_utils import (
    get_monthly_sales_trend, 
    get_profit_loss_trends,
    get_stockist_performance,
    get_expense_breakdown,
    get_cash_flow_data,
    get_marketing_spend,
    get_payroll_data,
    get_receivables_payables,
    get_custom_orders,
    get_top_stockists,
    get_alerts,
    get_product_profitability_proxy,
    get_sales_channel_summary,
    get_all_customers, # Fixed function
    get_all_stockists,
    get_all_products,
    apply_filters
)
import ui_components as ui

# Constants
LOGO_URL = "https://thekandleco.com/cdn/shop/files/logo_black.png?v=1685600000" # Placeholder if needed

st.set_page_config(
    page_title="🕯️ The Kandle Co",
    page_icon="🕯️",
    layout="wide", # Changed to wide for the dashboard layout
    initial_sidebar_state="expanded"
)

from views.login_view import show_login_page

# Initialize DB for Login
init_db()

# Session State for Filters
if 'selected_year' not in st.session_state:
    st.session_state.selected_year = 2024
if 'selected_months' not in st.session_state:
    st.session_state.selected_months = ['Jul']

# ================= LOGIN FLOW =================
if not st.session_state.get("authenticated", False):
    show_login_page()
    st.stop()

# Load Custom CSS (only after authentication)
ui.load_css()


# ================= DASHBOARD LAYOUT =================

# --- Sidebar ---
with st.sidebar:
    # Logo Section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try:
            st.image("assets/logo.jpg", width=120)
        except Exception:
            # Fallback if image not found (user hasn't saved it yet)
            st.markdown('<div style="text-align: center; margin-bottom: 2rem; color: white; font-family: Playfair Display; font-size: 1.5rem;">The Kandle Co.</div>', unsafe_allow_html=True)
    
    st.markdown('<div style="margin-bottom: 20px;"></div>', unsafe_allow_html=True) # Spacing
    
    # User Profile Section (Mock)
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 10px; padding: 10px; background: rgba(255,255,255,0.1); border-radius: 12px; margin-bottom: 2rem;">
        <div style="width: 40px; height: 40px; background: #ddd; border-radius: 50%; display: flex; align-items: center; justify-content: center;">👤</div>
        <div style="color: white;">
            <div style="font-size: 0.9rem; font-weight: bold;">Admin User</div>
            <div style="font-size: 0.7rem; opacity: 0.7;">View Profile</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    page = st.radio("Menu", ["Dashboard", "Sales", "Expenses", "Inventory", "Settings"], label_visibility="collapsed")
    
    st.markdown("---")
    
    # Calendar Widget Placeholder
    st.markdown("""
    <div class="calendar-widget">
        <div class="calendar-header">Aug 2024</div>
        <div style="display: grid; grid-template-columns: repeat(7, 1fr); gap: 5px; font-size: 0.7rem; color: #718096;">
            <div>S</div><div>M</div><div>T</div><div>W</div><div>T</div><div>F</div><div>S</div>
            <div></div><div></div><div></div><div></div><div>1</div><div>2</div><div>3</div>
            <div>4</div><div>5</div><div>6</div><div style="background: #38A169; color: white; border-radius: 50%;">7</div><div>8</div><div>9</div><div>10</div>
            <div>11</div><div>12</div><div>13</div><div>14</div><div>15</div><div>16</div><div>17</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()

# --- Main Content ---

# Top Row: Metric Cards
# Fetch Data for Cards
# Using Jul-2024 data as default since we just synced it
df_sales = get_monthly_sales_trend()
df_curr = apply_filters(df_sales, 2024, ['Jul'])

total_sales = df_curr['total_sales'].sum() if not df_curr.empty else 0
total_expenses = 0 # Placeholder until expense sync
net_profit = 0 # Placeholder

cols = st.columns(4)

with cols[0]:
    ui.metric_card("Total Balance", "$2,256", "Updated hour ago", "metric-card-1", icon="💰") # Placeholder currency
with cols[1]:
    ui.metric_card("Total Sales", f"Rs. {total_sales:,.0f}", "Jul-2024", "metric-card-2", icon="💼")
with cols[2]:
    ui.metric_card("Total Expenses", "$120", "Updated hour ago", "metric-card-3", icon="💸")
with cols[3]:
    ui.metric_card("Total Visitors", "3", "Updated hour ago", "metric-card-4", icon="👥")

# Row 2: Charts and Lists
c1, c2 = st.columns([2, 1])

with c1:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown('<h3>Observations</h3>', unsafe_allow_html=True)
    
    # Mock Observations
    ui.observation_item("Top Product: Burning Firewood", "2", 85)
    ui.observation_item("Stockist: Shams", "5", 65, color="#ECC94B")
    ui.observation_item("Inventory Alert: Glass Jars", "1", 25, color="#E53E3E")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Graph Section
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown('<h3>Sales Trend</h3>', unsafe_allow_html=True)
    
    if not df_sales.empty:
        fig = px.line(df_sales, x='month_year', y='total_sales', markers=True)
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(t=10, l=10, r=10, b=10),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='#eee'),
            height=250
        )
        fig.update_traces(line_color='#2F855A', line_width=3)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No sales data available for trend graph.")
        
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown('<h3>Stats</h3>', unsafe_allow_html=True)
    
    # Mock Stats
    ui.stats_item("Online", "52%", "#ECC94B", "🛒")
    ui.stats_item("Stockists", "21%", "#38A169", "🏢")
    ui.stats_item("Exhibitions", "74%", "#2B6CB0", "🎪")
    ui.stats_item("Custom", "14%", "#2D3748", "🎁")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Customer List
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown('<h3>Top Customers</h3>', unsafe_allow_html=True)
    
    df_cust = get_all_customers()
    if not df_cust.empty:
        for _, row in df_cust.head(4).iterrows():
            st.markdown(f"""
            <div style="display: flex; align-items: center; margin-bottom: 12px;">
                <div style="width: 30px; height: 30px; background: #f0f0f0; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 10px;">👤</div>
                <div style="flex-grow: 1;">
                    <div style="font-weight: 600; font-size: 0.85rem;">{row['customer_name']}</div>
                    <div style="font-size: 0.7rem; color: #888;">{row['order_count']} Orders</div>
                </div>
                <div style="font-weight: bold; font-size: 0.8rem;">{row['total_revenue']/1000:,.0f}k</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)