import streamlit as st
import data_utils
import plotly.express as px
import plotly.graph_objects as go # Added missing import

def load_view():
    st.markdown("## 📊 Cash Flow Intelligence")
    st.markdown("### Never Be Surprised by Cash")
    st.markdown("*Monitor your business's vital signs: inflows, outflows, and net cash position to ensure you always have enough runway to grow.*")
    
    # --- Global Filters ---
    selected_year = st.session_state.get('selected_year', 2024)
    selected_months = st.session_state.get('selected_months', ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    
    # --- Data Loading ---
    df_cash = data_utils.apply_filters(data_utils.get_cash_flow_data(), selected_year, selected_months)
    pay_df, rec_df = data_utils.get_receivables_payables()
    pay_df = data_utils.apply_filters(pay_df, selected_year, selected_months)
    rec_df = data_utils.apply_filters(rec_df, selected_year, selected_months)
    
    if df_cash.empty:
        st.error("No cash flow data available.")
        return

    # Cash is usually point-in-time (end of selected period)
    curr_cash_val = df_cash['net_cash'].iloc[-1] if not df_cash.empty else 0
    
    # --- KPIs ---
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Net Cash Position", f"Rs. {curr_cash_val:,.0f}", f"End of {selected_months[-1]} {selected_year}")
    with c2:
        # burn calculation could be more complex, keeping simple avg for selection
        avg_burn = 500000 
        runway = (curr_cash_val / avg_burn) if avg_burn > 0 else 0
        st.metric("Cash Runway (Est)", f"{runway:.1f} Months", "Avg Burn: 500k")
    with c3:
        tot_rec = rec_df['total_receivable'].sum() if not rec_df.empty else 0
        st.metric("Total Receivables", f"Rs. {tot_rec:,.0f}", "Pending Inflow")

    # --- Cash Trend ---
    st.markdown("### Cash Position Trend")
    fig_cash = px.area(df_cash, x="month_year", y="net_cash", markers=True,
                       labels={"net_cash": "Cash (Rs)", "month_year": "Month"},
                       template="plotly_white", color_discrete_sequence=['#10b981']) # Green for cash
    st.plotly_chart(fig_cash, use_container_width=True)
    
    # --- Inflow vs Outflow Proxy ---
    # Using Sales (Inflow) vs Admin Expenses (Outflow) as proxy
    df_sales = data_utils.apply_filters(data_utils.get_monthly_sales_trend(), selected_year, selected_months)
    df_exp = data_utils.apply_filters(data_utils.get_expense_breakdown(), selected_year, selected_months)
    
    st.markdown("### Monthly Inflow vs Outflow (Operational)")
    
    fig_io = go.Figure()
    fig_io.add_trace(go.Bar(x=df_sales['month_year'], y=df_sales['total_sales'], name='Inflow (Sales)', marker_color='#10b981'))
    fig_io.add_trace(go.Bar(x=df_exp['month_year'], y=df_exp['total_admin_expenses'], name='Outflow (Exp)', marker_color='#ef4444'))
    
    fig_io.update_layout(barmode='group', template="plotly_white")
    st.plotly_chart(fig_io, use_container_width=True)
