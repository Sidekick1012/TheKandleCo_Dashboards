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
    # Aggressive UI Injection for Sidebar
    st.markdown("""
        <style>
            /* Force Sidebar Toggle Buttons to be White */
            button[data-testid="stSidebarCollapseButton"], 
            button[kind="header"],
            [data-testid="stHeader"] button,
            header button svg {
                color: white !important;
                fill: white !important;
            }
            
            /* Aggressive Sidebar Reset */
            [data-testid="stSidebarContent"] {
                padding-top: 0rem !important;
                margin-top: 0rem !important;
            }
            
            [data-testid="stSidebarNav"] {
                padding-top: 0rem !important;
            }

            /* Logo Positioning - Move higher and center */
            .sidebar-logo-container {
                text-align: center;
                margin-top: -80px !important;
                margin-bottom: 20px !important;
            }
            .sidebar-logo-container img {
                width: 120px;
                filter: brightness(0) invert(1); /* Ensure logo is white if it's black */
            }

            /* Premium Logout Button */
            div.stButton > button:first-child {
                background: transparent !important;
                color: #ECC94B !important;
                border: 1px solid #ECC94B !important;
                border-radius: 8px !important;
                width: 100% !important;
                font-weight: 600 !important;
                text-transform: uppercase !important;
                letter-spacing: 1px !important;
                margin-top: 0.5rem !important;
            }
        </style>
    """, unsafe_allow_html=True)

    # Logo Section (Direct HTML for better control)
    st.markdown("""
        <div class="sidebar-logo-container">
            <img src="https://thekandleco.com/cdn/shop/files/logo_black.png?v=1685600000">
        </div>
    """, unsafe_allow_html=True)
    # --- Navigator ---
    st.markdown('<div class="sidebar-section-header" style="color: #ecc94b; font-weight: 600; font-size: 0.75rem; letter-spacing: 2px; opacity: 0.8;">NAVIGATOR</div>', unsafe_allow_html=True)
    page = st.radio("Menu", [
        "📊 Revenue Overview", 
        "📅 Seasonality Advisor", 
        "💰 Cash Flow Strategist",
        "🩺 Margin Doctor"
    ], label_visibility="collapsed")
    
    st.markdown("---")
    
    # --- Global Filters ---
    st.markdown('<div class="sidebar-section-header" style="color: #ecc94b; font-weight: 600; font-size: 0.75rem; letter-spacing: 2px; opacity: 0.8;">GLOBAL FILTERS</div>', unsafe_allow_html=True)
    
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
    st.markdown('<h1 class="main-title" style="font-size: 1.6rem;">📊 Revenue Overview</h1>', unsafe_allow_html=True)
    # Dashboard Header & Filter Context
    st.markdown(f"""
        <div style="background: rgba(236, 201, 75, 0.1); padding: 1rem; border-radius: 10px; border-left: 5px solid #ECC94B; margin-bottom: 2rem;">
            <p style="margin: 0; font-weight: 600; color: #ECC94B;">🔍 Filter Context: {st.session_state.selected_year} | {", ".join(st.session_state.selected_months) if st.session_state.selected_months else "Full Year"}</p>
            <p style="margin: 5px 0 0 0; font-size: 0.85rem; color: #718096;">All metrics below are <b>Synced</b> to your sidebar selection. This dashboard provides a comprehensive snapshot of your financial health, including real bank balance and net profitability.</p>
        </div>
    """, unsafe_allow_html=True)

    # Top Row: Metric Cards
    # Fetch Data for Cards
    df_sales = get_monthly_sales_trend()
    df_exp = get_expense_breakdown()
    df_cash = get_cash_flow_data()
    df_pl = get_profit_loss_trends()
    
    # Apply Filters
    df_sales_curr = apply_filters(df_sales, st.session_state.selected_year, st.session_state.selected_months)
    df_exp_curr = apply_filters(df_exp, st.session_state.selected_year, st.session_state.selected_months)
    df_cash_curr = apply_filters(df_cash, st.session_state.selected_year, st.session_state.selected_months)
    df_pl_curr = apply_filters(df_pl, st.session_state.selected_year, st.session_state.selected_months)
    
    # Calculate Totals
    total_sales = df_sales_curr['total_sales'].sum() if not df_sales_curr.empty else 0
    total_expenses = df_exp_curr['total_admin_expenses'].sum() if not df_exp_curr.empty else 0
    net_profit = df_pl_curr['net_profit_loss'].sum() if not df_pl_curr.empty else 0
    
    # For Balance, we take the latest month in the selection (data is DESC by default)
    current_balance = df_cash_curr.iloc[0]['net_cash'] if not df_cash_curr.empty else 0
    
    cols = st.columns(4)
    
    with cols[0]:
        ui.metric_card("Total Balance", f"Rs. {current_balance:,.0f}", "Cash + Bank", "metric-card-1", icon="💰") 
    with cols[1]:
        ui.metric_card("Total Sales", f"Rs. {total_sales:,.0f}", f"{st.session_state.selected_year} Selection", "metric-card-2", icon="💼")
    with cols[2]:
        ui.metric_card("Total Expenses", f"Rs. {total_expenses:,.0f}", "Admin & Shared", "metric-card-3", icon="💸")
    with cols[3]:
        # Calculate Margin
        margin = (net_profit / total_sales * 100) if total_sales > 0 else 0
        ui.metric_card("Net Profit", f"Rs. {net_profit:,.0f}", f"{margin:.1f}% Margin", "metric-card-4", icon="📈")
    
    # Row 2: Charts and Lists
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<h3>Critical Observations</h3>', unsafe_allow_html=True)
        st.markdown('<p style="color: #718096; font-size: 0.85rem; margin-top: -0.5rem; margin-bottom: 1.5rem;"><b>Meaning:</b> Ye section aapko batata hai ke aap apne Monthly Targets (<b>Rs. 1.5M per month</b>) aur Profitability goals ke kitne qareeb hain.</p>', unsafe_allow_html=True)
        
        # Calculate Target Progress
        # Let's assume a target of Rs. 1.5M per month
        n_months = len(st.session_state.selected_months)
        target = 1500000 * n_months
        progress = min(100, int((total_sales / target) * 100)) if target > 0 else 0
        
        ui.observation_item("Revenue Target Progress", f"Target: Rs. {target/1000000:.1f}M", progress)
        
        # Gross Margin Observation
        avg_gross = df_pl_curr['gross_margin_percentage'].mean() if not df_pl_curr.empty else 0
        margin_status = "Healthy" if avg_gross >= 60 else "Attention Required"
        ui.observation_item("Average Gross Margin", f"{margin_status} ({avg_gross:.1f}%)", int(avg_gross))
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Graph Section
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<h3>Sales Trend</h3>', unsafe_allow_html=True)
        st.markdown('<p style="color: #718096; font-size: 0.85rem; margin-top: -0.5rem; margin-bottom: 1rem;"><b>Meaning:</b> Ye graph aapki sales ki raftaar (Performance) dikhata hai aapke selected period ke liye.</p>', unsafe_allow_html=True)
        
        # Show trend for selected months
        df_trend = apply_filters(df_sales, st.session_state.selected_year, st.session_state.selected_months)
        
        if not df_trend.empty:
            # Sort chronologically (reverse DESC) for chart flow
            df_trend = df_trend.iloc[::-1]
            
            fig = px.line(df_trend, x='month_year', y='total_sales', markers=True)
            fig.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                margin=dict(t=10, l=10, r=10, b=10),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='#eee'),
                height=200
            )
            fig.update_traces(line_color='#2F855A', line_width=3)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No sales data available for trend graph.")
            
        st.markdown('</div>', unsafe_allow_html=True)
    
    with c2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<h3>Channel Mix</h3>', unsafe_allow_html=True)
        st.markdown('<p style="color: #718096; font-size: 0.85rem; margin-top: -0.5rem; margin-bottom: 1.5rem;"><b>Meaning:</b> Ye chart batata hai ke aapka paisa kahan se aa raha hai (Online, Shops, ya Exhibitions).</p>', unsafe_allow_html=True)
        
        # Calculate real stats
        if total_sales > 0:
            p_online = (df_sales_curr['online_sales'].sum() / total_sales) * 100
            p_stockist = (df_sales_curr['stockist_sales'].sum() / total_sales) * 100
            p_custom = (df_sales_curr['custom_order_sales'].sum() / total_sales) * 100
            p_exhibition = (df_sales_curr['exhibition_sales'].sum() / total_sales) * 100
        else:
            p_online = p_stockist = p_custom = p_exhibition = 0
            
        ui.stats_item("Online", f"{p_online:.0f}%", "#ECC94B", "🛒")
        ui.stats_item("Stockists", f"{p_stockist:.0f}%", "#38A169", "🏢")
        ui.stats_item("Custom", f"{p_custom:.0f}%", "#2D3748", "🎁")
        ui.stats_item("Exhibitions", f"{p_exhibition:.0f}%", "#2B6CB0", "🎪")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Customer List
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<h3>Top Customers</h3>', unsafe_allow_html=True)
        st.markdown('<p style="color: #718096; font-size: 0.85rem; margin-top: -0.5rem; margin-bottom: 1.5rem;"><b>Meaning:</b> Ye aapke VIP customers hain jo sabse zyada purchase karte hain.</p>', unsafe_allow_html=True)
        
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
    show_seasonality_view(st.session_state.selected_year, st.session_state.selected_months)

elif page == "💰 Cash Flow Strategist":
    show_cash_flow_view(st.session_state.selected_year, st.session_state.selected_months)

elif page == "🩺 Margin Doctor":
    show_unit_economics_view(st.session_state.selected_year, st.session_state.selected_months)
