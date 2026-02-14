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

from views.seasonality_view import show_seasonality_view
from views.cash_flow_view import show_cash_flow_view
from views.unit_economics_view import show_unit_economics_view

# --- Sidebar ---
with st.sidebar:
    # Logo Section
    import os
    try:
        logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div style="margin-top: -50px !important;">', unsafe_allow_html=True)
            st.image(logo_path, width=100)
            st.markdown('</div>', unsafe_allow_html=True)
    except Exception as e:
        # Fallback if image not found or fails to open
        st.markdown('<div style="text-align: center; margin-bottom: 2rem; color: white; font-family: Playfair Display; font-size: 1.5rem;">The Kandle Co.</div>', unsafe_allow_html=True)
    # --- Navigator ---
    st.markdown('<div style="color: #ecc94b; font-weight: 600; font-size: 0.75rem; letter-spacing: 2px; margin: 2rem 0 1rem 0; opacity: 0.8;">NAVIGATOR</div>', unsafe_allow_html=True)
    page = st.radio("Menu", [
        "📊 Revenue Overview", 
        "📅 Seasonality Advisor", 
        "💰 Cash Flow Strategist",
        "🩺 Margin Doctor"
    ], label_visibility="collapsed")
    
    st.markdown("---")
    
    # --- Global Filters ---
    st.markdown('<div style="color: #ecc94b; font-weight: 600; font-size: 0.75rem; letter-spacing: 2px; margin-bottom: 1.2rem; opacity: 0.8;">GLOBAL FILTERS</div>', unsafe_allow_html=True)
    
    # Year Selection
    years = [2024, 2025]
    curr_year_idx = years.index(st.session_state.selected_year) if st.session_state.selected_year in years else 0
    selected_year = st.selectbox("📅 Select Year", years, index=curr_year_idx)
    if selected_year != st.session_state.selected_year:
        st.session_state.selected_year = selected_year
        st.rerun()
        
    # Month Selection
    all_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    selected_months = st.multiselect("Select Months", all_months, default=st.session_state.selected_months)
    if selected_months != st.session_state.selected_months:
        st.session_state.selected_months = selected_months
        st.rerun()
    
    st.markdown("---")
    
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()

# --- Main Content Routing ---

if page == "📊 Revenue Overview":
    # Top Row: Metric Cards
    # Fetch Data for Cards
    df_sales = get_monthly_sales_trend()
    df_curr = apply_filters(df_sales, st.session_state.selected_year, st.session_state.selected_months)
    
    total_sales = df_curr['total_sales'].sum() if not df_curr.empty else 0
    total_expenses = 0 # Placeholder until expense sync
    net_profit = 0 # Placeholder
    
    cols = st.columns(4)
    
    with cols[0]:
        ui.metric_card("Total Balance", "Rs. 0", "Current Session", "metric-card-1", icon="💰") 
    with cols[1]:
        ui.metric_card("Total Sales", f"Rs. {total_sales:,.0f}", f"{st.session_state.selected_year} Selection", "metric-card-2", icon="💼")
    with cols[2]:
        ui.metric_card("Total Expenses", "Rs. 0", "Current Session", "metric-card-3", icon="💸")
    with cols[3]:
        ui.metric_card("Total Visitors", "0", "Current Session", "metric-card-4", icon="👥")
    
    # Row 2: Charts and Lists
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<h3>Observations</h3>', unsafe_allow_html=True)
        
        # Observe based on current selection
        ui.observation_item("Sales Goal", f"{st.session_state.selected_year}", 100 if total_sales > 0 else 0)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Graph Section
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<h3>Sales Trend</h3>', unsafe_allow_html=True)
        
        # Show trend for whole year or selected months
        df_trend = apply_filters(df_sales, st.session_state.selected_year, None) # Trend for whole year
        
        if not df_trend.empty:
            fig = px.line(df_trend, x='month_year', y='total_sales', markers=True)
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

elif page == "📅 Seasonality Advisor":
    show_seasonality_view()

elif page == "💰 Cash Flow Strategist":
    show_cash_flow_view()

elif page == "🩺 Margin Doctor":
    show_unit_economics_view()
