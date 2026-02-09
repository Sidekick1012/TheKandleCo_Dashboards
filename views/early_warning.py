import streamlit as st
import data_utils

def load_view():
    st.markdown("## 📊 Early Warning System")
    st.markdown("### The Proactive Alerts Dashboard")
    st.markdown("*Proactive alerts and anomaly detection that warn you about margin drops, stock risks, or cash flow issues before they become problems.*")
    
    # --- Global Filters ---
    selected_year = st.session_state.get('selected_year', 2024)
    selected_months = st.session_state.get('selected_months', ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    
    # --- Alerts Logic ---
    alerts = data_utils.get_alerts(selected_year, selected_months)
    
    if not alerts:
        st.success("✅ No critical alerts. Business is stable.")
    else:
        for alert in alerts:
            if alert['type'] == 'danger':
                st.error(f"🔴 {alert['message']}")
            elif alert['type'] == 'warning':
                st.warning(f"🟡 {alert['message']}")
            elif alert['type'] == 'info':
                st.info(f"🔵 {alert['message']}")
    
    # --- Watchlist Table ---
    st.markdown("### Performance Watchlist")
    
    # Check key metrics manually
    df_pl = data_utils.apply_filters(data_utils.get_profit_loss_trends(), selected_year, selected_months)
    
    # Get LAST YEAR same period for delta
    df_pl_ly = data_utils.apply_filters(data_utils.get_profit_loss_trends(), selected_year - 1, selected_months)
    
    if not df_pl.empty:
        curr_agg = df_pl.mean(numeric_only=True) # Average margins
        prev_year_agg = df_pl_ly.mean(numeric_only=True) if not df_pl_ly.empty else curr_agg
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            margin_val = curr_agg['gross_margin_percentage']
            margin_ly = prev_year_agg['gross_margin_percentage']
            delta_m = margin_val - margin_ly
            st.metric("Avg Gross Margin", f"{margin_val:.1f}%", 
                      delta=f"{delta_m:.1f}% vs LY", 
                      delta_color="normal")
            
        with col2:
             st.metric("Total Net Profit", f"Rs. {df_pl['net_profit_loss'].sum():,.0f}", "Selection Total")
             
        with col3:
             # Comparing total admin expenses to last year same period
             total_exp = df_pl['total_admin_expenses'].sum()
             total_exp_ly = df_pl_ly['total_admin_expenses'].sum() if not df_pl_ly.empty else total_exp
             exp_change = ((total_exp - total_exp_ly) / total_exp_ly * 100) if total_exp_ly > 0 else 0
             st.metric("Expense Variance", f"{exp_change:.1f}%", 
                       delta=f"{exp_change:.1f}% vs LY",
                       delta_color="inverse")

    st.markdown("---")
    st.caption("Auto-generated based on current month's performance vs historical patterns.")
