import streamlit as st
import data_utils
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def load_view():
    st.markdown("## 📊 Revenue & Sales Deep Dive")
    st.markdown("### Detailed Monthly & Seasonal Analysis")
    st.markdown("*In-depth analysis of sales trends, channel performance, and seasonal heatmaps to identify what drives your growth.*")
    
    # --- Global Filters ---
    selected_year = st.session_state.get('selected_year', 2024)
    selected_months = st.session_state.get('selected_months', ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    
    # --- Data Loading ---
    df_yoy = data_utils.get_yoy_growth_data() # YoY usually shows all, but we can filter within if needed
    df_sales = data_utils.apply_filters(data_utils.get_monthly_sales_trend(), selected_year, selected_months)
    
    if df_sales.empty:
        st.error("No data available.")
        return

    # --- Seasonality Heat Map ---
    st.markdown("### Seasonality Heat Map (Revenue)")
    if not df_yoy.empty:
        fig_heat = px.imshow(df_yoy, 
                             labels=dict(x="Year", y="Month", color="Revenue"),
                             text_auto=',.0f', aspect="auto",
                             color_continuous_scale='YlOrBr')
        st.plotly_chart(fig_heat, use_container_width=True)
    else:
        st.info("Need more than 12 months of data for YoY Heatmap.")

    # --- Revenue Trend Analysis ---
    st.markdown("### Revenue Performance Timeline")
    # Calculate moving average
    df_sales['MA_3'] = df_sales['total_sales'].rolling(window=3).mean()
    
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Bar(x=df_sales['month_year'], y=df_sales['total_sales'], name='Monthly Revenue', marker_color='#1a1a1a'))
    fig_trend.add_trace(go.Scatter(x=df_sales['month_year'], y=df_sales['MA_3'], name='3-Month Avg', line=dict(color='#D4AF37', width=3)))
    
    fig_trend.update_layout(template='plotly_white', xaxis_title='Month', yaxis_title='Revenue (Rs)')
    st.plotly_chart(fig_trend, use_container_width=True)
    
    # --- Revenue Concentration ---
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### Revenue Concentration by Channel")
        # SUM all sales for the selection period
        channels = ['online_sales', 'stockist_sales', 'custom_order_sales', 'exhibition_sales']
        vals = [df_sales[c].sum() for c in channels]
        names = [c.replace('_sales', '').title() for c in channels]
        
        fig_pie = px.pie(values=vals, names=names, hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with c2:
        st.markdown("### Average Order Value (Est) Trend")
        # Simulating AOV based on online sales / Est 100 orders
        df_sales['Est_AOV'] = df_sales['online_sales'] / 100 
        fig_aov = px.line(df_sales, x='month_year', y='Est_AOV', markers=True,
                          template='plotly_white', color_discrete_sequence=['#2563eb'])
        st.plotly_chart(fig_aov, use_container_width=True)
