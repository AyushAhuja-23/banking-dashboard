import streamlit as st
import pandas as pd
import plotly.express as px

# 1. IMPORT OUR CLEANING FUNCTION
from data_processing import load_and_clean_data

# 2. SET PAGE CONFIGURATION
st.set_page_config(page_title="Summary", page_icon="📊", layout="wide")

# 3. LOAD THE DATA
df = load_and_clean_data()

# 4. SAFETY CHECK
if not df.empty:
    st.title("Summary Dashboard")

    # 5. CLIENT DRILL-DOWN FILTER
    # This is the new, primary filter for this page.
    st.subheader("Client Drill-Down")
    
    # We create a list of all client names, plus "All Clients" at the start.
    client_list = ["All Clients"] + sorted(df['Name'].unique())
    
    selected_client = st.selectbox(
        "Select a Client to Drill Down (or 'All Clients' for default view):",
        options=client_list,
        index=0 # Default to "All Clients"
    )

    st.markdown("---")

    # 6. STANDARD FILTERS (with new logic)
    st.subheader("Standard Filters")
    # This logic disables the standard filters if a single client is selected.
    disable_filters = (selected_client != "All Clients")

    filter_col1, filter_col2, filter_col3 = st.columns(3)
    with filter_col1:
        relationship_options = ['All'] + list(df['Banking Relationship'].dropna().unique())
        selected_relationship = st.selectbox(
            "Banking Relationship", 
            options=relationship_options, 
            index=0, 
            disabled=disable_filters # New 'disabled' property
        )
    # ... (Same for the other two filters) ...
    with filter_col2:
        gender_options = ['All'] + list(df['Gender'].dropna().unique())
        selected_gender = st.selectbox(
            "Gender", 
            options=gender_options, 
            index=0, 
            disabled=disable_filters
        )
    with filter_col3:
        advisor_options = ['All'] + list(df['Investment Advisor'].dropna().unique())
        selected_advisor = st.selectbox(
            "Investment Advisor", 
            options=advisor_options, 
            index=0, 
            disabled=disable_filters
        )

    # 7. FILTER DATAFRAME (with new logic)
    df_filtered = df.copy()

    # If a specific client is selected, we *only* use that filter.
    if selected_client != "All Clients":
        df_filtered = df_filtered[df_filtered['Name'] == selected_client]
        st.info(f"Showing dashboard for: **{selected_client}**")
    else:
        # Otherwise, we use the standard 3 filters.
        if selected_relationship != 'All':
            df_filtered = df_filtered[df_filtered['Banking Relationship'] == selected_relationship]
        if selected_gender != 'All':
            df_filtered = df_filtered[df_filtered['Gender'] == selected_gender]
        if selected_advisor != 'All':
            df_filtered = df_filtered[df_filtered['Investment Advisor'] == selected_advisor]

    # 8. DISPLAY ALL KPIs
    # This code is the same, but it shows data for EITHER one client OR a group.
    st.subheader("Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    # ... (st.metric code for all 12 KPIs) ...
    with col1:
        st.metric(label="Total Clients", value=f"{df_filtered['Client ID'].nunique()}")
        st.metric(label="Total Deposit", value=f"${df_filtered['Total Deposit'].sum():,.2f}")
        st.metric(label="Total CC Amount", value=f"${df_filtered['Amount of Credit Cards'].sum():,.2f}")
    with col2:
        st.metric(label="Total Loan", value=f"${df_filtered['Total Loan'].sum():,.2f}")
        st.metric(label="Total Fees", value=f"${(df_filtered['Total Loan'] * df_filtered['Processing Fees']).sum():,.2f}")
        st.metric(label="Saving Account Amount", value=f"${df_filtered['Saving Accounts'].sum():,.2f}")
    with col3:
        st.metric(label="Bank Loan", value=f"${df_filtered['Bank Loans'].sum():,.2f}")
        st.metric(label="Bank Deposit", value=f"${df_filtered['Bank Deposits'].sum():,.2f}")
        st.metric(label="Foreign Currency Amount", value=f"${df_filtered['Foreign Currency Account'].sum():,.2f}")
    with col4:
        st.metric(label="Business Lending", value=f"${df_filtered['Business Lending'].sum():,.2f}")
        st.metric(label="Checking Account Amount", value=f"${df_filtered['Checking Accounts'].sum():,.2f}")
        st.metric(label="Engagement Days (Total)", value=f"{df_filtered['Engagment Days'].sum():,.0f}")
else:
    st.warning("Data could not be loaded.")