import streamlit as st
import pandas as pd
import plotly.express as px

# Import the main data processing function
from data_processing import load_and_clean_data

st.set_page_config(page_title="Advisor Performance", page_icon="💼", layout="wide")

# Load the clean data
df = load_and_clean_data()

if not df.empty:
    st.title("Investment Advisor Performance")

    # --- 1. Advisor Leaderboard (Table) ---
    st.subheader("Advisor Leaderboard")

    df_clients = df.groupby('Investment Advisor')['Client ID'].nunique().reset_index(name='Total Clients')
    df_financials = df.groupby('Investment Advisor')[['Total Deposit', 'Total Loan']].sum().reset_index()
    df_leaderboard = df_clients.merge(df_financials, on='Investment Advisor')
    df_leaderboard = df_leaderboard.sort_values(by='Total Clients', ascending=False)
    
    st.dataframe(
        df_leaderboard.set_index('Investment Advisor').style
        .format({
            'Total Clients': '{:,.0f}',
            'Total Deposit': '${:,.2f}',
            'Total Loan': '${:,.2f}'
        }),
        use_container_width=True
    )

    st.markdown("---")

    # --- 2. Charts Layout ---
    col1, col2 = st.columns(2)

    with col1:
        # --- 2a. Deposits by Advisor (Bar) ---
        st.subheader("Total Deposits by Advisor")
        df_deposits = df_leaderboard.sort_values(by='Total Deposit', ascending=False)
        fig_dep_bar = px.bar(
            df_deposits,
            x='Investment Advisor',
            y='Total Deposit',
            title='Total Deposits Managed by Advisor'
        )
        st.plotly_chart(fig_dep_bar, use_container_width=True)

        # --- 2b. Client Loyalty by Advisor (Stacked Bar) ---
        # --- CODE MODIFIED TO AVOID 'barnorm' ---
        st.subheader("Client Loyalty Mix by Advisor")
        df_loyalty_raw = df.groupby(['Investment Advisor', 'Loyalty Classification'])['Client ID'].count().reset_index(name='Client Count')
        # Calculate totals for each advisor
        df_totals = df_loyalty_raw.groupby('Investment Advisor')['Client Count'].sum().reset_index(name='Total Clients')
        # Merge totals back
        df_loyalty = df_loyalty_raw.merge(df_totals, on='Investment Advisor')
        # Calculate percentage
        df_loyalty['Percentage'] = df_loyalty['Client Count'] / df_loyalty['Total Clients']
        
        fig_loyalty_stack = px.bar(
            df_loyalty,
            x='Investment Advisor',
            y='Percentage', # Use Percentage for the y-axis
            color='Loyalty Classification',
            title='Client Loyalty Mix (Normalized)',
            labels={'Percentage': 'Percentage of Clients'}
        )
        # Format y-axis as percentage
        fig_loyalty_stack.update_layout(yaxis_tickformat=".0%") 
        st.plotly_chart(fig_loyalty_stack, use_container_width=True)

    with col2:
        # --- 2c. Loans by Advisor (Bar) ---
        st.subheader("Total Loans by Advisor")
        df_loans = df_leaderboard.sort_values(by='Total Loan', ascending=False)
        fig_loan_bar = px.bar(
            df_loans,
            x='Investment Advisor',
            y='Total Loan',
            title='Total Loans Managed by Advisor',
            color_discrete_sequence=['#ef553b'] # Use a different color
        )
        st.plotly_chart(fig_loan_bar, use_container_width=True)

        # --- 2d. Client Risk by Advisor (Stacked Bar) ---
        # --- CODE MODIFIED TO AVOID 'barnorm' ---
        st.subheader("Client Risk Mix by Advisor")
        df_risk_raw = df.groupby(['Investment Advisor', 'Risk Weighting'])['Client ID'].count().reset_index(name='Client Count')
        # Calculate totals for each advisor
        df_risk_totals = df_risk_raw.groupby('Investment Advisor')['Client Count'].sum().reset_index(name='Total Clients')
        # Merge totals back
        df_risk = df_risk_raw.merge(df_risk_totals, on='Investment Advisor')
        # Calculate percentage
        df_risk['Percentage'] = df_risk['Client Count'] / df_risk['Total Clients']

        fig_risk_stack = px.bar(
            df_risk,
            x='Investment Advisor',
            y='Percentage', # Use Percentage for the y-axis
            color='Risk Weighting',
            title='Client Risk Mix (Normalized)',
            labels={'Percentage': 'Percentage of Clients'}
        )
        # Format y-axis as percentage
        fig_risk_stack.update_layout(yaxis_tickformat=".0%")
        st.plotly_chart(fig_risk_stack, use_container_width=True)

else:
    st.warning("Data could not be loaded. Please check your data files.")