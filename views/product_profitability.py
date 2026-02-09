import streamlit as st
import data_utils
import plotly.express as px

def load_view():
    st.markdown("## 📊 Product Profitability Matrix")
    st.markdown("### Know Your Winners and Losers")
    st.markdown("*Identify your most profitable products and see which ones are driving volume versus which ones are pulling down margins.*")
    
    # --- Global Filters ---
    selected_year = st.session_state.get('selected_year', 2024)
    selected_months = st.session_state.get('selected_months', ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    
    # --- Data Loading ---
    # Using Proxy Data - apply_filters hook added for consistency
    df_prod = data_utils.apply_filters(data_utils.get_product_profitability_proxy(), selected_year, selected_months)
    
    if df_prod.empty:
        st.error("No product data available.")
        return

    # --- Quadrant Chart ---
    st.markdown("### Profitability Quadrant (Stars vs Dogs)")
    
    # Create the quadrant chart
    fig = px.scatter(df_prod, x="volume", y="margin", 
                     color="category", size="volume",
                     text="name",
                     labels={"volume": "Sales Volume (Units)", "margin": "Gross Margin (%)"},
                     template="plotly_white",
                     color_discrete_map={
                         "Star": "#D4AF37",         # Gold
                         "Cash Cow": "#2563eb",     # Blue
                         "Question Mark": "#9333ea", # Purple
                         "Dog": "#ef4444"           # Red
                     })
    
    # Add quadrant lines
    avg_vol = df_prod['volume'].mean()
    avg_marg = df_prod['margin'].mean()
    
    fig.add_hline(y=avg_marg, line_dash="dash", line_color="gray", annotation_text="Avg Margin")
    fig.add_vline(x=avg_vol, line_dash="dash", line_color="gray", annotation_text="Avg Volume")
    
    fig.update_traces(textposition='top center')
    fig.update_layout(height=600)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # --- Detail Table ---
    st.markdown("### Product Performance Details")
    st.dataframe(df_prod.style.highlight_max(axis=0, color='#d4af3733'), use_container_width=True)
    
    st.info("💡 **Insight**: Invest marketing spend in 'Stars'. Optimize costs for 'Cash Cows'. Evaluating 'Question Marks' for promotion or discontinuation.")
