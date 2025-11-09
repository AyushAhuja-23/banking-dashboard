import streamlit as st
import pandas as pd
import plotly.express as px

# 1. IMPORT OUR CLEANING FUNCTION
from data_processing import load_and_clean_data

# 2. SET PAGE CONFIGURATION
st.set_page_config(page_title="Deposit Analysis", page_icon="💵", layout="wide")

# 3. LOAD THE DATA
df = load_and_clean_data()

# 4. SAFETY CHECK
if not df.empty:
    st.title("Deposit Analysis")

    # 5. DEFINE FILTERS
    # Same 3 filters as the Loan Analysis page.
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    with filter_col1:
        relationship_options = ['All'] + list(df['Banking Relationship'].dropna().unique())
        selected_relationship = st.selectbox("Banking Relationship", options=relationship_options, index=0)
    with filter_col2:
        gender_options = ['All'] + list(df['Gender'].dropna().unique())
        selected_gender = st.selectbox("Gender", options=gender_options, index=0)
    with filter_col3:
        advisor_options = ['All'] + list(df['Investment Advisor'].dropna().unique())
        selected_advisor = st.selectbox("Investment Advisor", options=advisor_options, index=0)

    # 6. FILTER DATAFRAME
    df_filtered = df.copy()
    if selected_relationship != 'All':
        df_filtered = df_filtered[df_filtered['Banking Relationship'] == selected_relationship]
    if selected_gender != 'All':
        df_filtered = df_filtered[df_filtered['Gender'] == selected_gender]
    if selected_advisor != 'All':
        df_filtered = df_filtered[df_filtered['Investment Advisor'] == selected_advisor]

    # 7. DISPLAY KPIs
    # KPIs specific to deposits.
    kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
    with kpi_col1:
        st.metric(label="Total Deposit", value=f"${df_filtered['Total Deposit'].sum():,.2f}")
    with kpi_col2:
        st.metric(label="Bank Deposit", value=f"${df_filtered['Bank Deposits'].sum():,.2f}")
    with kpi_col3:
        st.metric(label="Foreign Currency Amount", value=f"${df_filtered['Foreign Currency Account'].sum():,.2f}")
    
    kpi_col4, kpi_col5 = st.columns(2)
    with kpi_col4:
        st.metric(label="Saving Account Amount", value=f"${df_filtered['Saving Accounts'].sum():,.2f}")
    with kpi_col5:
        st.metric(label="Checking Account Amount", value=f"${df_filtered['Checking Accounts'].sum():,.2f}")
        
    st.markdown("---")

    # 8. DISPLAY CHARTS
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        # 8a. Chart 1 (Treemap)
        st.subheader("Bank Deposit by Income Band")
        df_tree = df_filtered.groupby('Income Band')['Bank Deposits'].sum().reset_index()
        fig_tree = px.treemap(df_tree, path=['Income Band'], values='Bank Deposits')
        st.plotly_chart(fig_tree, use_container_width=True)

        # 8b. Chart 2 (Bar)
        st.subheader("Total Deposit by Engagement Timeframe")
        df_bar_eng = df_filtered.groupby('Engagement Timeframe')['Total Deposit'].sum().reset_index()
        st.bar_chart(df_bar_eng.set_index('Engagement Timeframe'))
    
    with chart_col2:
        # 8c. Chart 3 (Stacked Bar)
        st.subheader("Deposit Analysis by Nationality")
        # Group by Nationality and sum the main deposit types
        df_nat_stack = df_filtered.groupby('Nationality')[['Bank Deposits', 'Saving Accounts', 'Checking Accounts', 'Foreign Currency Account']].sum().reset_index()
        # We must "melt" the data to a long format for Plotly to stack it.
        df_nat_melted = df_nat_stack.melt(id_vars='Nationality', var_name='Account Type', value_name='Amount')
        fig_nat_stack = px.bar(df_nat_melted, x='Nationality', y='Amount', color='Account Type', title='Deposit Breakdown by Nationality')
        st.plotly_chart(fig_nat_stack, use_container_width=True)
else:
    st.warning("Data could not be loaded.")