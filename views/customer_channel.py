import streamlit as st
import data_utils
import plotly.express as px

def load_view():
    st.markdown("## 📊 Customer & Channel Analysis")
    st.markdown("### Who buys and where?")
    st.markdown("*A deep dive into your customer segments and sales channel performance to understand who your best customers are.*")
    
    # --- Global Filters ---
    selected_year = st.session_state.get('selected_year', 2024)
    selected_months = st.session_state.get('selected_months', ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    
    # --- Data Loading ---
    df_sales = data_utils.apply_filters(data_utils.get_monthly_sales_trend(), selected_year, selected_months)
    
    if df_sales.empty:
        st.error("No data available.")
        return
    
    # --- Channel Performance ---
    st.markdown("### Channel Revenue Breakdown")
    
    c1, c2 = st.columns(2)
    
    with c1:
        # Pie Chart - Aggregate Sum for the selection
        channels = ['online_sales', 'stockist_sales', 'custom_order_sales', 'exhibition_sales']
        vals = [df_sales[c].sum() for c in channels]
        names = [c.replace('_sales', '').title() for c in channels]
        
        fig_pie = px.pie(values=vals, names=names, 
                         color_discrete_sequence=px.colors.sequential.Bluyl)
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with c2:
        # Top Channel KPI from aggregate
        total_vals = sum(vals)
        if total_vals > 0:
            best_idx = vals.index(max(vals))
            best_ch = names[best_idx]
            st.metric("Top Performing Channel", best_ch, f"Rs. {vals[best_idx]:,.0f}")
            
            # B2B vs B2C Split from aggregate
            b2b = df_sales['stockist_sales'].sum() + df_sales['custom_order_sales'].sum()
            b2c = df_sales['online_sales'].sum() + df_sales['exhibition_sales'].sum()
            total = b2b + b2c
            st.metric("B2B vs B2C Split", f"{(b2b/total*100):.0f}% B2B" if total > 0 else "0% B2B", 
                      f"{(b2c/total*100):.0f}% B2C" if total > 0 else "0% B2C")
        else:
            st.info("No sales data available for this selection.")

    # --- Customer Segments (Proxy) ---
    st.markdown("### Top Stockists & Customers")
    
    col_s, col_c = st.columns(2)
    
    with col_s:
        st.markdown("### Top Stockists (Selection Sum)")
        # Filter stockist performance by Selection
        df_sp = data_utils.apply_filters(data_utils.get_stockist_performance(), selected_year, selected_months)
        if not df_sp.empty:
            df_ts = df_sp.groupby('stockist_name')['sales_amount'].sum().reset_index().sort_values('sales_amount', ascending=False).head(5)
            df_ts.reset_index(drop=True, inplace=True)
            df_ts.index = df_ts.index + 1  # Start from 1
            df_ts.index.name = 'Rank'
            df_ts.columns = ['Stockist Name', 'Sales Amount']
            df_ts['Sales Amount'] = df_ts['Sales Amount'].apply(lambda x: f"Rs. {x:,.0f}")
            st.dataframe(df_ts, use_container_width=True)
        else:
            st.info("No stockist data for selection.")
    
    with col_c:
        st.markdown("### Top Custom Clients")
        # Direct query fallback/mock filtered in memory
        df_tc = data_utils.get_custom_orders().sort_values('total_rev', ascending=False).head(5)
        
        if not df_tc.empty:
             st.bar_chart(df_tc.set_index('customer_name')['total_rev'])
