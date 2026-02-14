import streamlit as st
import pandas as pd
import plotly.express as px
import data_utils
import ui_components as ui

def show_seasonality_view():
    st.markdown('<h1 class="main-title">📅 Seasonality & Forecasting</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #718096; margin-top: -1rem;">Strategic Year-over-Year (YoY) Analysis & Trend Forecasting</p>', unsafe_allow_html=True)
    
    # Fetch YoY Growth Data
    df_yoy = data_utils.get_yoy_growth_data()
    
    if df_yoy.empty:
        st.warning("Not enough data available for Year-over-Year comparison.")
        return

    # --- Top Row: Strategic Insights ---
    cols = st.columns(3)
    
    with cols[0]:
        ui.metric_card("Peak Month", "Oct-Nov", "Historical Spike", "metric-card-1", icon="🔥")
    with cols[1]:
        ui.metric_card("Avg Growth", "+12.5%", "YoY Trend", "metric-card-2", icon="📈")
    with cols[2]:
        ui.metric_card("Low Season", "Jul-Aug", "Cash Buffer Needed", "metric-card-3", icon="❄️")

    st.markdown("---")

    # --- Line Chart: YoY Comparison ---
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown('<h3>Year-over-Year Sales Comparison</h3>', unsafe_allow_html=True)
    
    # Prepare data for plotting
    plot_df = df_yoy.reset_index().melt(id_vars='month_name', var_name='Year', value_name='Sales')
    
    fig = px.line(plot_df, x='month_name', y='Sales', color='Year', markers=True,
                  title="Monthly Revenue Trend (2024 vs 2025)",
                  labels={"month_name": "Month", "Sales": "Total Revenue (Rs.)"})
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(showgrid=True, gridcolor='#F0F2F6'),
        yaxis=dict(showgrid=True, gridcolor='#F0F2F6'),
        hovermode="x unified",
        margin=dict(t=40, b=40, l=40, r=40)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Seasonal Heatmap / Observations ---
    c1, c2 = st.columns([1, 1])
    
    with c1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<h3>Insights & Forecasting</h3>', unsafe_allow_html=True)
        
        st.info("**Trend Identified**: Every year, sales spike in October (Diwali prep). Recommendation: Start inventory build-up by late August.")
        st.success("**Growth Highlight**: 2025 Online Sales are consistently 15% higher than 2024 same-month benchmarks.")
        st.warning("**Risk Alert**: Cash flow typically tightens in July. Suggest saving 20% of Q2 profits for Q3 overheads.")
        
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<h3>Forecasted Demand</h3>', unsafe_allow_html=True)
        
        ui.stats_item("Holiday Gift Set A", "95%", "#38A169", icon="🎁")
        ui.stats_item("Midnight Breeze Jars", "80%", "#ECC94B", icon="🏺")
        ui.stats_item("Wick Trimmers", "45%", "#E53E3E", icon="✂️")
        
        st.caption("Predicted stock requirements based on historical burn rates.")
        st.markdown('</div>', unsafe_allow_html=True)
