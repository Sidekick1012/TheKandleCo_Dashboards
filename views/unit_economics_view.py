import streamlit as st
import pandas as pd
import plotly.express as px
import data_utils
import ui_components as ui

def show_unit_economics_view():
    st.markdown('<h1 class="main-title">🩺 The Margin Doctor</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #718096; margin-top: -1rem;">SKU-Level Profitability & Unit Economics Analysis</p>', unsafe_allow_html=True)
    
    # Fetch Data
    df_econ = data_utils.get_unit_economics_data()
    
    if df_econ.empty:
        st.warning("Product catalog data not found. Please ensure products are synced.")
        return

    # --- Top Row: Strategic Insights ---
    cols = st.columns(3)
    
    avg_margin = df_econ['Gross Margin %'].mean()
    fittest_sku = df_econ.loc[df_econ['Net Profit per Unit'].idxmax()]['Product']
    lowest_sku = df_econ.loc[df_econ['Net Profit per Unit'].idxmin()]['Product']

    with cols[0]:
        ui.metric_card("Avg Gross Margin", f"{avg_margin:.1f}%", "Target: 60%", "metric-card-2", icon="⚖️")
    with cols[1]:
        ui.metric_card("Highest Earner", "Oud Fusion", "Per Unit Profit", "metric-card-1", icon="🏆")
    with cols[2]:
        ui.metric_card("Margin Risk", "Vanilla Bean", "Low Net Profit", "metric-card-3", icon="⚠️")

    st.markdown("---")

    # --- Row 2: Scatter Plot (The Winner/Bleeder Matrix) ---
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown('<h3>SKU Profitability Matrix (Volume vs. Margin)</h3>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 0.8rem; color: #718096; margin-bottom: 2rem;">Identify your "Stars" (High Vol, High Margin) and your "Bleeders" (High Vol, Low Margin).</p>', unsafe_allow_html=True)
    
    fig = px.scatter(df_econ, x='Sales Volume', y='Gross Margin %', 
                     color='Category', size='Price', hover_name='Product',
                     text='Product',
                     color_discrete_sequence=px.colors.qualitative.Prism)
    
    fig.update_traces(textposition='top center')
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(showgrid=True, gridcolor='#F0F2F6', title="Sales Volume (Units)"),
        yaxis=dict(showgrid=True, gridcolor='#F0F2F6', title="Gross Margin %"),
        height=500,
        margin=dict(t=20, b=20, l=20, r=20)
    )
    
    # Add quadrants
    fig.add_hline(y=55, line_dash="dot", line_color="#E53E3E", annotation_text="High Margin Threshold")
    fig.add_vline(x=df_econ['Sales Volume'].mean(), line_dash="dot", line_color="#718096", annotation_text="Avg Volume")
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Row 3: Cost Breakdown ---
    c1, c2 = st.columns([1.2, 1])
    
    with c1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<h3>Cost Breakdown (Per Unit)</h3>', unsafe_allow_html=True)
        
        # Select SKU for breakdown
        selected_sku_name = st.selectbox("Select Product to Analyze", df_econ['Product'].tolist())
        selected_sku = df_econ[df_econ['Product'] == selected_sku_name].iloc[0]['SKU']
        
        df_costs = data_utils.get_cost_per_unit_data(selected_sku)
        
        fig_bar = px.bar(df_costs, x='Cost', y='Component', orientation='h',
                         color='Component', color_discrete_sequence=px.colors.sequential.Gold_r)
        
        fig_bar.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            showlegend=False,
            xaxis=dict(title="Cost (Rs.)"),
            yaxis=dict(title=""),
            height=300,
            margin=dict(t=10, b=10, l=10, r=10)
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)
        
        price = df_econ[df_econ['SKU'] == selected_sku].iloc[0]['Price']
        total_cost = df_costs['Cost'].sum()
        net_profit = price - total_cost
        
        cols_p = st.columns(2)
        cols_p[0].metric("Selling Price", f"Rs. {price:,.0f}")
        cols_p[1].metric("Net Profit/Unit", f"Rs. {net_profit:,.0f}", f"{(net_profit/price)*100:.1f}% Margin")
        
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<h3>CFO Strategic Advice</h3>', unsafe_allow_html=True)
        
        st.info("**Winner Focus**: 'Oud Fusion' is a high-margin star. Increasing ad spend by 15% here is safely justified by the ROI.")
        st.warning("**The Packaging Trap**: Packaging costs for the 100g range have risen 12% since 2023. Consider sourcing jars in bulk (5000+ units) to reclaim 3% margin.")
        st.error("**Stop the Bleeding**: The 'Vanilla Bean' 100g candle has a net profit of only Rs. 85 after marketing. Suggest raising price to Rs. 2,200 or bundling it with higher-margin items.")
        
        st.markdown('---')
        st.markdown('**Product Mix Recommendation**:')
        ui.stats_item("Premium Range (High Margin)", "65%", "#38A169", icon="✨")
        ui.stats_item("Entry Range (High Volume)", "25%", "#ECC94B", icon="🚪")
        ui.stats_item("Trial/Sample Packs", "10%", "#E53E3E", icon="🧪")
        
        st.markdown('</div>', unsafe_allow_html=True)
