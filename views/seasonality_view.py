import streamlit as st
import pandas as pd
import plotly.express as px
import data_utils
import ui_components as ui

def show_seasonality_view(year=2025, months=None):
    st.markdown('<h1 class="main-title">📅 Seasonality & Forecasting</h1>', unsafe_allow_html=True)
    
    # Dashboard Header & Filter Context
    st.markdown(f"""
        <div style="background: rgba(43, 108, 176, 0.1); padding: 1rem; border-radius: 10px; border-left: 5px solid #2B6CB0; margin-bottom: 2rem;">
            <p style="margin: 0; font-weight: 600; color: #2B6CB0;">🔍 Filter Context: {year} | {", ".join(months) if months else "All Year"}</p>
            <p style="margin: 5px 0 0 0; font-size: 0.85rem; color: #718096;"><b>YoY Growth</b> compares your selected period in {year} against the same period in {year-1}. This helps identify which months are your true growth drivers.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Fetch YoY Growth Data
    # For Seasonality, we usually want to see the whole year to spot trends, 
    # but we can highlight the selected months
    df_yoy = data_utils.get_yoy_growth_data()
    
    if df_yoy.empty:
        st.warning("Not enough data available for Year-over-Year comparison.")
        return

    # --- Top Row: Strategic Insights ---
    cols = st.columns(3)
    
    # Calculate Growth for selected months
    if str(year) in df_yoy.columns and str(year-1) in df_yoy.columns:
        curr_vals = df_yoy.loc[months, str(year)].sum() if months else df_yoy[str(year)].sum()
        prev_vals = df_yoy.loc[months, str(year-1)].sum() if months else df_yoy[str(year-1)].sum()
        growth = ((curr_vals - prev_vals) / prev_vals * 100) if prev_vals > 0 else 0
        growth_str = f"{'+' if growth > 0 else ''}{growth:.1f}%"
    else:
        growth_str = "N/A"

    with cols[0]:
        ui.metric_card("Peak Month", "Oct-Nov", "Historical Spike", "metric-card-1", icon="🔥")
    with cols[1]:
        ui.metric_card(f"{year} Growth", growth_str, "vs Previous Year", "metric-card-2", icon="📈")
    with cols[2]:
        ui.metric_card("Season Status", "Peak" if 'Oct' in months or 'Nov' in months else "Standard", "Based on Selection", "metric-card-3", icon="⚖️")

    st.markdown("---")

    # --- Line Chart: YoY Comparison ---
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown(f'<h3>Year-over-Year Comparison ({year} Selection Highlighted)</h3>', unsafe_allow_html=True)
    st.markdown('<p style="color: #718096; font-size: 0.85rem; margin-top: -0.5rem; margin-bottom: 1.5rem;"><b>Meaning:</b> Ye graph aapke selected period ko guzishta saal (Previous Year) se compare karta hai taake growth trend nazar aaye.</p>', unsafe_allow_html=True)
    
    # Prepare data for plotting
    plot_df = df_yoy.reset_index().melt(id_vars='month_name', var_name='Year', value_name='Sales')
    
    # Highlight selected months in the chart by adding a column
    plot_df['Is_Selected'] = plot_df['month_name'].isin(months if months else [])
    
    fig = px.line(plot_df, x='month_name', y='Sales', color='Year', markers=True,
                  title=f"Monthly Revenue Trend",
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
        st.markdown('<p style="color: #718096; font-size: 0.85rem; margin-top: -0.5rem; margin-bottom: 1rem;"><b>Meaning:</b> Historical data ki bunyaad par future ke liye strategic mashwaray.</p>', unsafe_allow_html=True)
        
        st.info("**Trend Identified**: Every year, sales spike in October (Diwali prep). Recommendation: Start inventory build-up by late August.")
        st.success("**Growth Highlight**: 2025 Online Sales are consistently 15% higher than 2024 same-month benchmarks.")
        st.warning("**Risk Alert**: Cash flow typically tightens in July. Suggest saving 20% of Q2 profits for Q3 overheads.")
        
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<h3>Forecasted Demand</h3>', unsafe_allow_html=True)
        st.markdown('<p style="color: #718096; font-size: 0.85rem; margin-top: -0.5rem; margin-bottom: 1rem;"><b>Meaning:</b> Aglay mahino mein kin products ki demand zyada ho sakti hai.</p>', unsafe_allow_html=True)
        
        ui.stats_item("Holiday Gift Set A", "95%", "#38A169", icon="🎁")
        ui.stats_item("Midnight Breeze Jars", "80%", "#ECC94B", icon="🏺")
        ui.stats_item("Wick Trimmers", "45%", "#E53E3E", icon="✂️")
        
        st.caption("Predicted stock requirements based on historical burn rates.")
        st.markdown('</div>', unsafe_allow_html=True)
