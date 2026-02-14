import streamlit as st
import pandas as pd
import plotly.express as px
import data_utils
import ui_components as ui

def show_cash_flow_view():
    st.markdown('<h1 class="main-title">💰 Cash Flow Advisor</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #718096; margin-top: -1rem;">Strategic Liquidity & Burn Rate Management</p>', unsafe_allow_html=True)
    
    # Fetch Data
    df_sales = data_utils.get_monthly_sales_trend()
    df_expenses = data_utils.get_expense_breakdown()
    df_cash = data_utils.get_cash_flow_data()
    
    # --- Top Row: Liquidity Metrics ---
    cols = st.columns(4)
    
    current_cash = df_cash.iloc[-1]['net_cash'] if not df_cash.empty else 0
    avg_burn = df_expenses['total_admin_expenses'].mean() if not df_expenses.empty else 1
    runway = current_cash / avg_burn if avg_burn > 0 else 0

    with cols[0]:
        ui.metric_card("Total Liquidity", f"Rs. {current_cash:,.0f}", "Bank + Hand", "metric-card-1", icon="🏦")
    with cols[1]:
        ui.metric_card("Monthly Burn", f"Rs. {avg_burn:,.0f}", "Avg Expenses", "metric-card-3", icon="🔥")
    with cols[2]:
        ui.metric_card("Cash Runway", f"{runway:.1f} Mo", "Survival Time", "metric-card-2", icon="⏳")
    with cols[3]:
        ui.metric_card("Days to Pay", "12 Days", "Payment Cycle", "metric-card-4", icon="💳")

    st.markdown("---")

    # --- Area Chart: Revenue vs Expenses ---
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown('<h3>The "Survival" Bridge: Revenue vs. Expenses</h3>', unsafe_allow_html=True)
    
    # Merge Sales and Expenses for Comparison
    df_comp = pd.merge(df_sales[['month_year', 'total_sales']], 
                       df_expenses[['month_year', 'total_admin_expenses']], 
                       on='month_year')
    
    df_plot = df_comp.melt(id_vars='month_year', var_name='Metric', value_name='Amount')
    df_plot['Metric'] = df_plot['Metric'].replace({'total_sales': 'Revenue', 'total_admin_expenses': 'Expenses'})
    
    fig = px.area(df_plot, x='month_year', y='Amount', color='Metric',
                  color_discrete_map={'Revenue': '#38A169', 'Expenses': '#E53E3E'},
                  title="Monthly Revenue vs operational Burn",
                  labels={"month_year": "Month", "Amount": "Amount (Rs.)"})
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        hovermode="x unified",
        margin=dict(t=40, b=40, l=40, r=40)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Strategic Advice ---
    c1, c2 = st.columns([1, 1])
    
    with c1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<h3>CFO Observations</h3>', unsafe_allow_html=True)
        
        st.warning("**Inventory Trap**: We have Rs. 500k tied in stockist receivables. Action: Follow up with 'Luxe Living' for faster settlements.")
        st.success("**Operational Health**: Fixed costs (Rent, Salaries) are covered by Online Sales alone. 100% of Exhibition sales are pure surplus.")
        st.info("**Forward Look**: Suggesting a 10% reduction in Variable Ad Spend in February to conserve cash for March manufacturing.")
        
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<h3>Liability Status</h3>', unsafe_allow_html=True)
        
        ui.stats_item("Accounts Payable", "Rs. 120k", "#E53E3E", icon="🧾")
        ui.stats_item("Outstanding Loans", "Rs. 0", "#38A169", icon="🕊️")
        ui.stats_item("Upcoming Payroll", "Rs. 240k", "#ECC94B", icon="👥")
        
        st.markdown('</div>', unsafe_allow_html=True)
