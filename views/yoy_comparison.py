import streamlit as st
import data_utils
import plotly.express as px
import pandas as pd

def load_view():
    st.markdown("## 📊 Year-over-Year Comparative Analysis")
    st.markdown("### Are You Actually Growing?")
    st.markdown("*A direct comparison of your current performance against the same period last year to measure genuine growth and progress.*")
    
    # --- Global Filters ---
    selected_year = st.session_state.get('selected_year', 2024)
    selected_months = st.session_state.get('selected_months', ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    
    # --- Data Loading ---
    df_yoy = data_utils.get_yoy_growth_data()
    # Filter YoY pivot by selected months
    if not df_yoy.empty:
        df_yoy = df_yoy.reindex(selected_months)
    
    if df_yoy.empty:
        st.warning("Insufficient data for Year-over-Year analysis.")
        return

    # --- Growth Table ---
    st.markdown("### Comparative Performance Table")
    # Replace NaN with dash for better display
    df_display = df_yoy.fillna('-')
    st.dataframe(df_display.style.highlight_max(axis=1, color='#d4af3733'), use_container_width=True)
    
    # --- Monthly Comparison Chart ---
    st.markdown("### Month-on-Month Same Period Comparison")
    
    # Transform for plotting
    df_plot = df_yoy.reset_index()
    df_melt = df_plot.melt(id_vars='month_name', var_name='Year', value_name='Revenue')
    
    fig = px.bar(df_melt, x='month_name', y='Revenue', color='Year', barmode='group',
                 labels={"month_name": "Month", "Revenue": "Revenue (Rs)"},
                 template="plotly_white",
                 color_discrete_sequence=['#cbd5e1', '#D4AF37']) # Grey for old, Gold for new
    
    st.plotly_chart(fig, use_container_width=True)
