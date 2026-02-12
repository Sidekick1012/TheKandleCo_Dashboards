import streamlit as st
import data_utils
import plotly.express as px
import pandas as pd

def load_view():
    st.markdown("## 📇 Customer & Product Directory")
    st.markdown("### Complete Business Directory")
    st.markdown("*A comprehensive view of all customers, stockists, and sales channels in one place.*")
    
    # Create tabs for better organization
    tab1, tab2, tab3 = st.tabs(["👥 Customers", "🏪 Stockists/Partners", "📊 Sales Channels"])
    
    # ==================== TAB 1: CUSTOMERS ====================
    with tab1:
        st.markdown("### 📋 All Customers (Custom Orders)")
        
        # Load customer data
        df_customers = data_utils.get_all_customers()
        
        if df_customers.empty:
            st.info("No customer data available.")
        else:
            # Summary metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Customers", len(df_customers))
            with col2:
                total_rev = df_customers['total_revenue'].sum()
                st.metric("Total Revenue", f"Rs. {total_rev:,.0f}")
            with col3:
                avg_order = df_customers['total_orders'].mean()
                st.metric("Avg Order Value", f"Rs. {avg_order:,.0f}")
            
            st.markdown("---")
            
            # Format the dataframe for display
            df_display = df_customers.copy()
            df_display.columns = ['Customer Name', 'Total Revenue', 'Total Orders', 'Order Count']
            df_display['Total Revenue'] = df_display['Total Revenue'].apply(lambda x: f"Rs. {x:,.0f}")
            df_display['Total Orders'] = df_display['Total Orders'].apply(lambda x: f"Rs. {x:,.0f}")
            
            # Display table
            st.dataframe(df_display, use_container_width=True, hide_index=True)
            
            # Chart: Top customers
            st.markdown("### 📊 Top 10 Customers by Revenue")
            df_top = df_customers.head(10)
            fig = px.bar(df_top, x='customer_name', y='total_revenue',
                        labels={'customer_name': 'Customer', 'total_revenue': 'Revenue (Rs)'},
                        color='total_revenue',
                        color_continuous_scale='Blues')
            st.plotly_chart(fig, use_container_width=True)
    
    # ==================== TAB 2: STOCKISTS ====================
    with tab2:
        st.markdown("### 🏪 All Stockists/Sales Partners")
        
        # Load stockist data
        df_stockists = data_utils.get_all_stockists()
        
        if df_stockists.empty:
            st.info("No stockist data available.")
        else:
            # Summary metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Stockists", len(df_stockists))
            with col2:
                total_sales = df_stockists['total_sales'].sum()
                st.metric("Total Sales", f"Rs. {total_sales:,.0f}")
            with col3:
                avg_months = df_stockists['active_months'].mean()
                st.metric("Avg Active Months", f"{avg_months:.1f}")
            
            st.markdown("---")
            
            # Format the dataframe for display
            df_display = df_stockists.copy()
            df_display.columns = ['Stockist Name', 'Total Sales', 'Active Months']
            df_display['Total Sales'] = df_display['Total Sales'].apply(lambda x: f"Rs. {x:,.0f}")
            
            # Display table
            st.dataframe(df_display, use_container_width=True, hide_index=True)
            
            # Chart: Top stockists
            st.markdown("### 📊 Top 10 Stockists by Sales")
            df_top = df_stockists.head(10)
            fig = px.bar(df_top, x='stockist_name', y='total_sales',
                        labels={'stockist_name': 'Stockist', 'total_sales': 'Sales (Rs)'},
                        color='total_sales',
                        color_continuous_scale='Greens')
            st.plotly_chart(fig, use_container_width=True)
    
    # ==================== TAB 3: SALES CHANNELS ====================
    with tab3:
        st.markdown("### 📊 Sales Channels Summary")
        
        # Load sales data
        df_sales = data_utils.get_sales_channel_summary()
        
        if df_sales.empty:
            st.info("No sales data available.")
        else:
            # Calculate totals for each channel
            total_online = df_sales['online_sales'].sum()
            total_stockist = df_sales['stockist_sales'].sum()
            total_custom = df_sales['custom_order_sales'].sum()
            total_exhibition = df_sales['exhibition_sales'].sum()
            
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Online Sales", f"Rs. {total_online:,.0f}")
            with col2:
                st.metric("Stockist Sales", f"Rs. {total_stockist:,.0f}")
            with col3:
                st.metric("Custom Orders", f"Rs. {total_custom:,.0f}")
            with col4:
                st.metric("Exhibitions", f"Rs. {total_exhibition:,.0f}")
            
            st.markdown("---")
            
            # Pie chart: Channel distribution
            st.markdown("### 🥧 Sales Distribution by Channel")
            channel_data = {
                'Channel': ['Online', 'Stockist', 'Custom Orders', 'Exhibitions'],
                'Sales': [total_online, total_stockist, total_custom, total_exhibition]
            }
            df_channels = pd.DataFrame(channel_data)
            
            fig_pie = px.pie(df_channels, values='Sales', names='Channel',
                            color_discrete_sequence=px.colors.sequential.RdBu)
            st.plotly_chart(fig_pie, use_container_width=True)
            
            # Recent months data
            st.markdown("### 📅 Recent Sales by Channel (Last 6 Months)")
            df_recent = df_sales.head(6)
            df_display = df_recent.copy()
            df_display.columns = ['Month', 'Online', 'Stockist', 'Custom', 'Exhibition', 'Total']
            
            # Format currency
            for col in ['Online', 'Stockist', 'Custom', 'Exhibition', 'Total']:
                df_display[col] = df_display[col].apply(lambda x: f"Rs. {x:,.0f}")
            
            st.dataframe(df_display, use_container_width=True, hide_index=True)
