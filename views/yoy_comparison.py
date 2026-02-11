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

    # --- Growth Heatmap ---
    st.markdown("### Comparative Performance Heatmap")
    
    import plotly.graph_objects as go
    
    # Prepare data
    df_heatmap = df_yoy.copy()
    
    # Get years and months
    years = df_heatmap.columns.tolist()
    months = df_heatmap.index.tolist()
    
    # Prepare values and text
    z_values = []
    text_values = []
    
    for year in years:
        year_values = []
        year_text = []
        for month in months:
            val = df_heatmap.loc[month, year]
            if pd.isna(val):
                year_values.append(0)  # For coloring
                year_text.append('None')
            else:
                year_values.append(val)
                year_text.append(f'Rs. {val:,.0f}')
        z_values.append(year_values)
        text_values.append(year_text)
    
    # Create heatmap with graph_objects
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=z_values,
        x=months,
        y=years,
        text=text_values,
        texttemplate='%{text}',
        textfont={"size": 10},
        colorscale='YlOrRd',
        showscale=True,
        hoverongaps=False
    ))
    
    fig_heatmap.update_layout(
        title='Sales Performance by Year and Month',
        xaxis_title='Month',
        yaxis_title='Year',
        height=300
    )
    
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
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
