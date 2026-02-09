import streamlit as st
import data_utils
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def load_view():
    st.markdown("## 📊 Cost Structure & Margin Analysis")
    st.markdown("### Where Is Your Money Going?")
    st.markdown("*A detailed breakdown of operating expenses, COGS, and margin trends to help you optimize business efficiency.*")
    
    # --- Global Filters ---
    selected_year = st.session_state.get('selected_year', 2024)
    selected_months = st.session_state.get('selected_months', ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    
    # --- Data Loading ---
    df_pl = data_utils.apply_filters(data_utils.get_profit_loss_trends(), selected_year, selected_months)
    df_exp = data_utils.apply_filters(data_utils.get_expense_breakdown(), selected_year, selected_months)
    
    if df_pl.empty:
        st.error("No data available.")
        return

    # --- Waterfall Chart ---
    st.markdown(f"### Cost Structure Waterfall ({selected_year}: {', '.join(selected_months)})")
    
    # Calculate aggregates for the selected period
    agg_sales = df_pl['total_sales'].sum()
    agg_cogs = df_pl['total_cogs'].sum()
    agg_admin = df_pl['total_admin_expenses'].sum()
    agg_net = df_pl['net_profit_loss'].sum()
    
    fig_waterfall = go.Figure(go.Waterfall(
        orientation = "v",
        measure = ["relative", "relative", "relative", "total"],
        x = ["Revenue", "COGS", "Admin Expenses", "Net Profit"],
        textposition = "outside",
        text = [f"{agg_sales/1000:.1f}k", f"-{agg_cogs/1000:.1f}k", f"-{agg_admin/1000:.1f}k", f"{agg_net/1000:.1f}k"],
        y = [agg_sales, -agg_cogs, -agg_admin, agg_net],
        connector = {"line":{"color":"rgb(63, 63, 63)"}},
        increasing = {"marker":{"color":"#D4AF37"}},
        decreasing = {"marker":{"color":"#1a1a1a"}},
        totals = {"marker":{"color":"#2563eb"}}
    ))
    fig_waterfall.update_layout(template="plotly_white", yaxis_title="Amount (Rs)")
    st.plotly_chart(fig_waterfall, use_container_width=True)

    # --- Margin Trend ---
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### Margin Trend (Gross vs Net)")
        fig_margin = px.line(df_pl, x="month_year", y=["gross_margin_percentage", "net_margin_percentage"],
                             labels={"value": "Margin (%)", "month_year": "Month", "variable": "Type"},
                             template="plotly_white",
                             color_discrete_map={"gross_margin_percentage": "#D4AF37", "net_margin_percentage": "#1a1a1a"})
        st.plotly_chart(fig_margin, use_container_width=True)
        
    with c2:
        st.markdown("### Expense Composition")
        # Summing up all expenses for the pie chart - Filter for numeric only to avoid sum() errors
        numeric_df = df_exp.select_dtypes(include=['number'])
        exp_cols = [c for c in numeric_df.columns if c not in ['id', 'total_admin_expenses'] and numeric_df[c].sum() > 0]
        exp_sums = numeric_df[exp_cols].sum().sort_values(ascending=False).head(6) 
        
        fig_pie = px.pie(values=exp_sums.values, names=[c.replace('_', ' ').title() for c in exp_sums.index], hole=0.3,
                         color_discrete_sequence=px.colors.sequential.YlOrBr_r)
        st.plotly_chart(fig_pie, use_container_width=True)
