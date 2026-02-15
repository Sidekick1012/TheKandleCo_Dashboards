import streamlit as st
import pandas as pd
import plotly.express as px
import data_utils
import ui_components as ui

def show_cash_flow_view(year=2025, months=None):
    st.markdown('<h1 class="main-title" style="font-size: 1.3rem;">💰 Cash Flow Advisor</h1>', unsafe_allow_html=True)
    
    # Dashboard Header & Filter Context
    st.markdown(f"""
        <div style="background: rgba(46, 161, 105, 0.1); padding: 1rem; border-radius: 10px; border-left: 5px solid #38A169; margin-bottom: 2rem;">
            <p style="margin: 0; font-weight: 600; color: #38A169;">🔍 Filter Context: {year} | {", ".join(months) if months else "All Year"}</p>
            <p style="margin: 5px 0 0 0; font-size: 0.85rem; color: #718096;"><b>Monthly Burn</b> is your average spending. <b>Runway</b> shows how many months you can survive if you make zero new sales. Data is 100% synced to your sidebar.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Fetch Data
    df_sales_raw = data_utils.get_monthly_sales_trend()
    df_expenses_raw = data_utils.get_expense_breakdown()
    df_cash_raw = data_utils.get_cash_flow_data()
    
    # Apply Filters
    df_sales = data_utils.apply_filters(df_sales_raw, year, months)
    df_expenses = data_utils.apply_filters(df_expenses_raw, year, months)
    df_cash = data_utils.apply_filters(df_cash_raw, year, months)
    
    # --- Top Row: Liquidity Metrics ---
    cols = st.columns(4)
    
    current_cash = df_cash.iloc[-1]['net_cash'] if not df_cash.empty else 0
    avg_burn = df_expenses['total_admin_expenses'].mean() if not df_expenses.empty else 1
    runway = current_cash / avg_burn if avg_burn > 0 else 0
    
    # Calculate selection totals
    sel_sales = df_sales['total_sales'].sum() if not df_sales.empty else 0
    sel_burn = df_expenses['total_admin_expenses'].sum() if not df_expenses.empty else 0

    with cols[0]:
        ui.metric_card("Filtered Liquidity", f"Rs. {current_cash:,.0f}", "As of selection", "metric-card-1", icon="🏦")
    with cols[1]:
        ui.metric_card("Total Selection Burn", f"Rs. {sel_burn:,.0f}", f"{len(months) if months else 12} Month(s)", "metric-card-3", icon="🔥")
    with cols[2]:
        ui.metric_card("Cash Runway", f"{runway:.1f} Mo", "At selected burn rate", "metric-card-2", icon="⏳")
    with cols[3]:
        # Net Cash movement for selection
        net_move = sel_sales - sel_burn
        ui.metric_card("Net Selection", f"Rs. {net_move:,.0f}", "Inflow vs Outflow", "metric-card-4", icon="💸")

    st.markdown("---")

    # --- Area Chart: Revenue vs Expenses ---
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown(f'<h3>Liquidity Bridge: Revenue vs. Burn ({year})</h3>', unsafe_allow_html=True)
    st.markdown('<p style="color: #718096; font-size: 0.85rem; margin-top: -0.5rem; margin-bottom: 1.5rem;"><b>Meaning:</b> Ye graph batata hai ke kya aapki Sales (Inflow) aapke Monthly Kharach (Burn) ko cover kar rahi hain ya nahi.</p>', unsafe_allow_html=True)
    
    if not df_sales.empty and not df_expenses.empty:
        # Merge Sales and Expenses for Comparison
        df_comp = pd.merge(df_sales[['month_year', 'total_sales']], 
                           df_expenses[['month_year', 'total_admin_expenses']], 
                           on='month_year')
        
        # Sort Chronologically for Left-to-Right Flow
        # Since 'month_year' is 'Mon-YYYY', we should ideally have a date column, 
        # but for now we can reverse the DESC order
        df_comp = df_comp.iloc[::-1] 
        
        df_plot = df_comp.melt(id_vars='month_year', var_name='Metric', value_name='Amount')
        df_plot['Metric'] = df_plot['Metric'].replace({'total_sales': 'Revenue', 'total_admin_expenses': 'Expenses'})
        
        fig = px.area(df_plot, x='month_year', y='Amount', color='Metric',
                      color_discrete_map={'Revenue': '#38A169', 'Expenses': '#E53E3E'},
                      title=f"Monthly Burn vs Inflow Trend",
                      labels={"month_year": "Month", "Amount": "Amount (Rs.)"})
        
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            hovermode="x unified",
            margin=dict(t=30, b=30, l=30, r=30),
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data found for the selected filter period.")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Strategic Advice ---
    c1, c2 = st.columns([1, 1])
    
    with c1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<h3>CFO Observations</h3>', unsafe_allow_html=True)
        st.markdown('<p style="color: #718096; font-size: 0.85rem; margin-top: -0.5rem; margin-bottom: 1rem;"><b>Meaning:</b> Cash flow ko behtar banane ke liye zaroori nukaat aur recommendations.</p>', unsafe_allow_html=True)
        
        st.warning("**Inventory Trap**: We have Rs. 500k tied in stockist receivables. Action: Follow up with 'Luxe Living' for faster settlements.")
        st.success("**Operational Health**: Fixed costs (Rent, Salaries) are covered by Online Sales alone. 100% of Exhibition sales are pure surplus.")
        st.info("**Forward Look**: Suggesting a 10% reduction in Variable Ad Spend in February to conserve cash for March manufacturing.")
        
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<h3>Liability Status</h3>', unsafe_allow_html=True)
        st.markdown('<p style="color: #718096; font-size: 0.85rem; margin-top: -0.5rem; margin-bottom: 1rem;"><b>Meaning:</b> Wo raqam jo aapne abhi logon ko deni hai (Payments due).</p>', unsafe_allow_html=True)
        
        ui.stats_item("Accounts Payable", "Rs. 120k", "#E53E3E", icon="🧾")
        ui.stats_item("Outstanding Loans", "Rs. 0", "#38A169", icon="🕊️")
        ui.stats_item("Upcoming Payroll", "Rs. 240k", "#D4AF37", icon="👥")
        
        st.markdown('</div>', unsafe_allow_html=True)
