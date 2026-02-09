import streamlit as st
import data_utils
import plotly.express as px
import pandas as pd

def load_view():
    st.markdown("## 📊 Executive Command Center")
    st.markdown("### The 60-Second Business Health Check")
    st.markdown("*A high-level overview of business health, tracking total revenue, profit margins, and cash position at a glance.*")
    
    # --- Global Filters ---
    selected_year = st.session_state.get('selected_year', 2024)
    selected_months = st.session_state.get('selected_months', ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    
    # --- Data Loading ---
    df_sales = data_utils.apply_filters(data_utils.get_monthly_sales_trend(), selected_year, selected_months)
    df_pl = data_utils.apply_filters(data_utils.get_profit_loss_trends(), selected_year, selected_months)
    df_cash = data_utils.apply_filters(data_utils.get_cash_flow_data(), selected_year, selected_months)
    
    # Get aggregates for current selection
    total_revenue = df_sales['total_sales'].sum()
    avg_gross_margin = df_pl['gross_margin_percentage'].mean() if not df_pl.empty else 0
    avg_net_margin = df_pl['net_margin_percentage'].mean() if not df_pl.empty else 0
    current_cash = df_cash['net_cash'].iloc[-1] if not df_cash.empty else 0 # Cash is usually point-in-time
    
    # --- YoY Comparison for KPIs ---
    # Fetch data for LAST YEAR
    prev_year = selected_year - 1
    df_sales_ly = data_utils.apply_filters(data_utils.get_monthly_sales_trend(), prev_year, selected_months)
    total_rev_ly = df_sales_ly['total_sales'].sum() if not df_sales_ly.empty else 0
    
    # --- KPIs ---
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        # Revenue vs Selection Same Period Last Year
        delta_rev = 0
        if total_rev_ly > 0:
            delta_rev = ((total_revenue - total_rev_ly) / total_rev_ly * 100)
        
        delta_label = f"vs {prev_year} (Same Months)"
        st.metric("Total Revenue", f"Rs. {total_revenue:,.0f}", f"{delta_rev:.1f}% {delta_label}")
        
    with c2:
        # Gross Margin (Average for selection)
        st.metric("Avg Gross Margin", f"{avg_gross_margin:.1f}%", "Target: >60%")
        
    with c3:
        # Net Margin (Average for selection)
        st.metric("Avg Net Margin", f"{avg_net_margin:.1f}%", "Target: >20%")
        
    with c4:
        # Cash Position (Current selection end)
        st.metric("Cash Position", f"Rs. {current_cash:,.0f}", "Point-in-time")

    st.markdown("---")
    
    # --- Charts ---
    c_chart1, c_chart2 = st.columns([2, 1])
    
    with c_chart1:
        st.markdown(f"### Revenue Trend ({selected_year})")
        fig = px.line(df_sales, x='month_year', y='total_sales', markers=True, 
                      template='plotly_white', line_shape='spline')
        fig.update_traces(line_color='#D4AF37', line_width=3)
        st.plotly_chart(fig, use_container_width=True)
        
    with c_chart2:
        st.markdown("### Top Products (Selection Sum)")
        # Using proxy data for now
        # In a real app we'd filter product sales by the same year/months
        df_prod = data_utils.get_product_profitability_proxy().sort_values('volume', ascending=False).head(5)
        st.table(df_prod[['name', 'volume']])
