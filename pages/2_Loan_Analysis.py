import streamlit as st
import pandas as pd
import plotly.express as px

# 1. IMPORT OUR CLEANING FUNCTION
# We are in a subfolder (pages), so we import from the parent folder.
from data_processing import load_and_clean_data

# 2. SET PAGE CONFIGURATION
st.set_page_config(page_title="Loan Analysis", page_icon="💰", layout="wide")

# 3. LOAD THE DATA
df = load_and_clean_data()

# 4. SAFETY CHECK
if not df.empty:
    st.title("Loan Analysis")

    # 5. DEFINE FILTERS
    # This page has 3 dropdown filters.
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    with filter_col1:
        # Get a list of unique values from the column for the options
        relationship_options = ['All'] + list(df['Banking Relationship'].dropna().unique())
        selected_relationship = st.selectbox("Banking Relationship", options=relationship_options, index=0)
    with filter_col2:
        gender_options = ['All'] + list(df['Gender'].dropna().unique())
        selected_gender = st.selectbox("Gender", options=gender_options, index=0)
    with filter_col3:
        advisor_options = ['All'] + list(df['Investment Advisor'].dropna().unique())
        selected_advisor = st.selectbox("Investment Advisor", options=advisor_options, index=0)

    # 6. FILTER DATAFRAME
    # Same logic as 1_Home.py, but for our 3 new filters.
    df_filtered = df.copy()
    if selected_relationship != 'All':
        df_filtered = df_filtered[df_filtered['Banking Relationship'] == selected_relationship]
    if selected_gender != 'All':
        df_filtered = df_filtered[df_filtered['Gender'] == selected_gender]
    if selected_advisor != 'All':
        df_filtered = df_filtered[df_filtered['Investment Advisor'] == selected_advisor]
    
    # 7. DISPLAY KPIs
    # These KPIs are specific to the Loan Analysis page.
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    with kpi_col1:
        st.metric(label="Total Loan", value=f"${df_filtered['Total Loan'].sum():,.2f}")
    with kpi_col2:
        st.metric(label="Bank Loan", value=f"${df_filtered['Bank Loans'].sum():,.2f}")
    with kpi_col3:
        st.metric(label="Business Lending", value=f"${df_filtered['Business Lending'].sum():,.2f}")
    with kpi_col4:
        st.metric(label="Credit Cards Balance", value=f"${df_filtered['Credit Card Balance'].sum():,.2f}")
        
    st.markdown("---")

    # 8. DISPLAY CHARTS
    # We create two columns for the chart layout.
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        # 8a. Chart 1 (Bar)
        st.subheader("Bank Loan by Banking Relationship")
        # We must group the data before plotting.
        df_bar = df_filtered.groupby('Banking Relationship')['Bank Loans'].sum().reset_index()
        fig_bar = px.bar(df_bar, x='Banking Relationship', y='Bank Loans', text=df_bar['Bank Loans'].apply(lambda x: f'${x:,.0f}'))
        st.plotly_chart(fig_bar, use_container_width=True)

        # 8b. Chart 2 (Donut)
        st.subheader("Bank Loan by Income Band")
        df_donut = df_filtered.groupby('Income Band')['Bank Loans'].sum().reset_index()
        fig_donut = px.pie(df_donut, names='Income Band', values='Bank Loans', hole=0.5)
        st.plotly_chart(fig_donut, use_container_width=True)
    
    with chart_col2:
        # 8c. Chart 3 (Treemap)
        st.subheader("Bank Loan by Nationality")
        df_tree = df_filtered.groupby('Nationality')['Bank Loans'].sum().reset_index()
        fig_tree = px.treemap(df_tree, path=['Nationality'], values='Bank Loans')
        st.plotly_chart(fig_tree, use_container_width=True)

        # 8d. Chart 4 (Bar)
        st.subheader("Total Loan by Engagement Timeframe")
        df_bar_eng = df_filtered.groupby('Engagement Timeframe')['Total Loan'].sum().reset_index()
        # st.bar_chart is a simple, built-in chart.
        st.bar_chart(df_bar_eng.set_index('Engagement Timeframe'))
else:
    st.warning("Data could not be loaded.")