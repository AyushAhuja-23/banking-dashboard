import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# 1. IMPORT OUR CLEANING FUNCTION
from data_processing import load_and_clean_data

# 2. SET PAGE CONFIGURATION
st.set_page_config(
    page_title="Banking Dashboard - Home",
    page_icon="🏦",
    layout="wide"
)

# 3. LOAD THE DATA
df = load_and_clean_data()

# 4. SAFETY CHECK
if not df.empty:
    
    # 5. PAGE LAYOUT
    st.title("Banking Dashboard")
    st.markdown("This dashboard provides an overview of key banking metrics.")

    # 6. DEFINE FILTERS
    st.subheader("Filters")
    filter_col1, filter_col2 = st.columns(2)
    
    with filter_col1:
        selected_time = st.radio(
            "Time Selection (based on 'Joined Bank')",
            ["All Time", "Last 30 D", "Last 90 D", "Last 6 M", "Last 12 M"],
            horizontal=True
        )
    
    with filter_col2:
        selected_gender = st.radio(
            "Gender",
            ["Female", "Male"],
            index=0, # Default to "Female"
            horizontal=True
        )

    st.markdown("---")
    
    # 7. FILTER DATAFRAME
    df_filtered = df.copy()
    
    # Apply the Gender filter
    if selected_gender:
        df_filtered = df_filtered[df_filtered['Gender'] == selected_gender]

    # --- THIS IS THE FIX ---
    # We find the latest date in the dataset to use as our "today".
    data_max_date = df['Joined Bank'].max()
    
    # Now we filter relative to the data's latest date.
    if selected_time == "Last 30 D":
        df_filtered = df_filtered[df_filtered['Joined Bank'] >= (data_max_date - timedelta(days=30))]
    elif selected_time == "Last 90 D":
        df_filtered = df_filtered[df_filtered['Joined Bank'] >= (data_max_date - timedelta(days=90))]
    elif selected_time == "Last 6 M":
        df_filtered = df_filtered[df_filtered['Joined Bank'] >= (data_max_date - timedelta(days=180))]
    elif selected_time == "Last 12 M":
        df_filtered = df_filtered[df_filtered['Joined Bank'] >= (data_max_date - timedelta(days=365))]
    # 'All Time' needs no filter
    
    # 8. CALCULATE KPIs
    kpi_total_clients = df_filtered['Client ID'].nunique()
    kpi_total_loan = df_filtered['Total Loan'].sum()
    kpi_total_deposit = df_filtered['Total Deposit'].sum()
    kpi_total_fees = (df_filtered['Total Loan'] * df_filtered['Processing Fees']).sum()
    kpi_total_cc_amount = df_filtered['Amount of Credit Cards'].sum()
    kpi_saving_account = df_filtered['Saving Accounts'].sum()

    # 9. DISPLAY KPIs
    kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
    
    with kpi_col1:
        st.metric(label="Total Clients", value=f"{kpi_total_clients}")
        st.metric(label="Total Deposit", value=f"${kpi_total_deposit:,.2f}")

    with kpi_col2:
        st.metric(label="Total Loan", value=f"${kpi_total_loan:,.2f}")
        st.metric(label="Total Fees", value=f"${kpi_total_fees:,.2f}")

    with kpi_col3:
        st.metric(label="Total CC Amount", value=f"${kpi_total_cc_amount:,.2f}")
        st.metric(label="Saving Account Amount", value=f"${kpi_saving_account:,.2f}")
            
else:
    st.warning("Data could not be loaded. Please check your data files.")