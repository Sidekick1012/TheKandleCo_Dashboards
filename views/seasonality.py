import streamlit as st
import data_utils
import plotly.express as px
import pandas as pd # Ensure pandas is imported

def load_view():
    st.markdown("## 📊 Seasonality & Demand Planning")
    st.markdown("### Predict Before You React")
    st.markdown("*Predictive insights into seasonal demand patterns to help you plan your stock levels and marketing well in advance.*")
    
    # --- Global Filters ---
    selected_year = st.session_state.get('selected_year', 2024)
    selected_months = st.session_state.get('selected_months', ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    
    # --- Data Loading ---
    df_yoy = data_utils.get_yoy_growth_data() # This covers all years for overlay
    
    if df_yoy.empty:
        st.warning("Insufficient historical data for seasonality analysis.")
        return

    # --- Seasonal Revenue Pattern ---
    st.markdown("### Seasonal Revenue Pattern (Multi-Year Overlay)")
    
    # Reset index to make 'month_name' a column for plotting
    df_plot = df_yoy.reset_index()
    
    # Melt for Plotly
    df_melt = df_plot.melt(id_vars='month_name', var_name='Year', value_name='Revenue')
    
    fig = px.line(df_melt, x='month_name', y='Revenue', color='Year', markers=True,
                  labels={"month_name": "Month", "Revenue": "Revenue (Rs)"},
                  template="plotly_white",
                  color_discrete_sequence=['#cbd5e1', '#64748b', '#D4AF37']) # Light, Dark, Gold for current
    
    st.plotly_chart(fig, use_container_width=True)
    
    # --- Peak Season Analysis ---
    st.markdown("### Peak Season Pre-Planning Guide")
    
    seasons = [
        {"Season": "Valentine's", "Period": "Feb 1-14", "Prep Start": "Jan 15", "Action": "Stock Gifts & Red Wax"},
        {"Season": "Mother's Day", "Period": "May 1-12", "Prep Start": "Apr 1", "Action": "Floral Scents Bundles"},
        {"Season": "Diwali", "Period": "Oct-Nov", "Prep Start": "Sep 1", "Action": "Maximize Inventory & Packaging"},
        {"Season": "Christmas", "Period": "Dec 1-25", "Prep Start": "Nov 1", "Action": "Holiday Scents & Gift Sets"}
    ]
    st.table(pd.DataFrame(seasons))
