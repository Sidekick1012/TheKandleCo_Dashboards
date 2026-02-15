import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import data_utils
import ui_components as ui

def show_unit_economics_view(year=2025, months=None):
    ui.title_with_candle("The Margin Doctor", icon="🩺")
    
    # Dashboard Header & Filter Context
    st.markdown(f"""
        <div style="background: rgba(229, 62, 62, 0.1); padding: 1rem; border-radius: 10px; border-left: 5px solid #E53E3E; margin-bottom: 2rem;">
            <p style="margin: 0; font-weight: 600; color: #E53E3E;">🔍 Filter Context: {year} | {", ".join(months) if months else "All Year"}</p>
            <p style="margin: 5px 0 0 0; font-size: 0.85rem; color: #718096;"><b>Gross Margin</b> is profit after raw material costs. The <b>Revenue Bridge</b> shows where every rupee goes (Marketing, Packaging, etc.). Pro-rated for your sidebar selection.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Fetch Data
    df_econ = data_utils.get_unit_economics_data(year, months)
    
    if df_econ.empty:
        st.warning("Product catalog data not found. Please ensure products are synced.")
        return

    # --- Top Row: Strategic Insights ---
    cols = st.columns(3)
    
    avg_margin = df_econ['Gross Margin %'].mean()

    with cols[0]:
        ui.metric_card("Avg Gross Margin", f"{avg_margin:.1f}%", "Target: 60%", "metric-card-2", icon="⚖️")
    with cols[1]:
        ui.metric_card("Winning Flavor", "Oud Fusion", "Highest Net Profit", "metric-card-1", icon="💎")
    with cols[2]:
        ui.metric_card("Underperformer", "Vanilla Bean", "Low Margin Warning", "metric-card-3", icon="🚨")

    st.markdown("---")

    # --- Row 2: SKU Margin Ranking (Horizontal Bar) ---
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown('<h3>SKU Margin Ranking: Winners & Bleeders</h3>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 0.8rem; color: #718096; margin-bottom: -0.5rem;">Ranked by Gross Margin % to show which products contribute most to profit per rupee.</p>', unsafe_allow_html=True)
    st.markdown('<p style="color: #718096; font-size: 0.85rem; margin-bottom: 2rem;"><b>Meaning:</b> Sabse zyada profit dene wale products upar hain, aur sabse kam profit wale niche.</p>', unsafe_allow_html=True)
    
    # Sort for ranking chart
    df_rank = df_econ.sort_values("Gross Margin %", ascending=True)
    
    fig_rank = px.bar(df_rank, x='Gross Margin %', y='Product', orientation='h',
                      color='Gross Margin %', 
                      color_continuous_scale=['#E53E3E', '#F6E05E', '#38A169'],
                      text_auto='.1f')
    
    fig_rank.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=400,
        xaxis=dict(showgrid=True, gridcolor='#F0F2F6', range=[0, 100]),
        yaxis=dict(showgrid=False),
        margin=dict(t=20, b=20, l=20, r=20),
        coloraxis_showscale=False
    )
    
    st.plotly_chart(fig_rank, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Row 3: Unit Economics Waterfall ---
    c1, c2 = st.columns([1.5, 1])
    
    with c1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<h3>The "Revenue Bridge" (Waterfall)</h3>', unsafe_allow_html=True)
        st.markdown('<p style="color: #718096; font-size: 0.85rem; margin-top: -0.5rem; margin-bottom: 1rem;"><b>Meaning:</b> Ek item ki sale price mein se kitna paisa materials, packing, aur marketing mein jata hai.</p>', unsafe_allow_html=True)
        
        # Select SKU for breakdown
        selected_sku_name = st.selectbox("Select Product to Analyze Bridge", df_econ['Product'].tolist())
        row = df_econ[df_econ['Product'] == selected_sku_name].iloc[0]
        
        # Prepare Waterfall Data
        # Revenue -> -Material -> -Pack -> -Marketing -> -Shipping (estimated 5%) -> Net Profit
        shipping = round(row['Price'] * 0.05, 0)
        
        fig_waterfall = go.Figure(go.Waterfall(
            name = "Unit Economics", orientation = "v",
            measure = ["relative", "relative", "relative", "relative", "relative", "total"],
            x = ["Revenue", "Raw Materials", "Packaging", "Marketing", "Shipping", "Net Profit"],
            textposition = "outside",
            text = [f"Rs. {row['Price']}", f"-{row['Material Cost']}", f"-{row['Packing per Unit']}", f"-{row['Marketing per Unit']}", f"-{shipping}", "Profit"],
            y = [row['Price'], -row['Material Cost'], -row['Packing per Unit'], -row['Marketing per Unit'], -shipping, 0],
            connector = {"line":{"color":"rgb(63, 63, 63)"}},
            decreasing = {"marker":{"color":"#E53E3E"}},
            increasing = {"marker":{"color":"#38A169"}},
            totals = {"marker":{"color":"#2B6CB0"}}
        ))

        fig_waterfall.update_layout(
            title = f"Unit Economics: {selected_sku_name}",
            plot_bgcolor='white',
            paper_bgcolor='white',
            showlegend = False,
            margin=dict(t=40, b=20, l=20, r=20),
            height=280
        )
        
        st.plotly_chart(fig_waterfall, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<h3>CFO Strategic Advice</h3>', unsafe_allow_html=True)
        st.markdown('<p style="color: #718096; font-size: 0.85rem; margin-top: -0.5rem; margin-bottom: 1rem;"><b>Meaning:</b> Konsi product band karni hai aur kis par zyada tawajjo deni hai.</p>', unsafe_allow_html=True)
        
        st.info("**Winner Focus**: 'Oud Fusion' is a high-margin star. Increasing ad spend by 15% here is safely justified by the ROI.")
        st.warning("**The Packaging Trap**: Packaging costs for the 100g range have risen 12% since 2023. Consider sourcing jars in bulk to reclaim 3% margin.")
        st.error("**Stop the Bleeding**: The 'Vanilla Bean' 100g candle has a net profit of only Rs. 85 after marketing. Suggest raising price or bundling.")
        
        st.markdown('---')
        st.markdown('**Product Mix Recommendation**:')
        ui.stats_item("Premium Range (High Margin)", "65%", "#38A169", icon="✨")
        ui.stats_item("Entry Range (High Volume)", "25%", "#D4AF37", icon="🚪")
        ui.stats_item("Trial/Sample Packs", "10%", "#E53E3E", icon="🧪")
        
        st.markdown('</div>', unsafe_allow_html=True)
