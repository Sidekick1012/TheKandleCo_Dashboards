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
    
    # Prepare data for heatmap
    df_heatmap = df_yoy.copy()
    
    # Create text labels with "None" for missing values
    text_labels = df_heatmap.applymap(lambda x: 'None' if pd.isna(x) else f'Rs. {x:,.0f}')
    
    # Replace NaN with 0 for color scaling (won't show in text)
    df_heatmap_values = df_heatmap.fillna(0)
    
    # Create heatmap
    fig_heatmap = px.imshow(
        df_heatmap_values.T,  # Transpose so years are rows
        labels=dict(x="Month", y="Year", color="Sales (Rs)"),
        x=df_heatmap_values.index.tolist(),
        y=df_heatmap_values.columns.tolist(),
        color_continuous_scale='YlOrRd',  # Yellow to Red
        text_auto=False,  # We'll add custom text
        aspect='auto'
    )
    
    # Add custom text annotations
    for i, year in enumerate(df_heatmap_values.columns):
        for j, month in enumerate(df_heatmap_values.index):
            fig_heatmap.add_annotation(
                text=text_labels.loc[month, year],
                x=j, y=i,
                showarrow=False,
                font=dict(color='black' if df_heatmap_values.loc[month, year] < df_heatmap_values.max().max()/2 else 'white')
            )
    
    fig_heatmap.update_layout(
        height=400,
        xaxis_title="Month",
        yaxis_title="Year"
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
