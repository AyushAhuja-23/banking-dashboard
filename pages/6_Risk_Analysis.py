import streamlit as st
import pandas as pd
import plotly.express as px

# 1. IMPORT OUR CLEANING FUNCTION
from data_processing import load_and_clean_data

# 2. SET PAGE CONFIGURATION
st.set_page_config(page_title="Risk & Loyalty", page_icon="🛡️", layout="wide")

# 3. LOAD THE DATA
df = load_and_clean_data()

# 4. SAFETY CHECK
if not df.empty:
    st.title("Risk & Loyalty Analysis")
    st.markdown("Analyze client risk profiles and loyalty classifications.")

    # 5. PAGE LAYOUT
    col1, col2 = st.columns(2)

    with col1:
        # 6. Chart 1: Client Risk Profile (Pie)
        st.subheader("Client Risk Profile")
        # .value_counts() gets the counts for each risk category
        risk_counts = df['Risk Weighting'].value_counts().reset_index()
        risk_counts.columns = ['Risk Weighting', 'Count']
        
        fig_risk = px.pie(
            risk_counts,
            names='Risk Weighting',
            values='Count',
            title='Distribution of Client Risk Weighting'
        )
        st.plotly_chart(fig_risk, use_container_width=True)

        # 7. Chart 2: Engagement by Loyalty (Box Plot)
        st.subheader("Engagement by Loyalty")
        # A box plot is perfect for comparing the distribution
        # (min, max, median, quartiles) of a number across categories.
        fig_box = px.box(
            df,
            x='Loyalty Classification',
            y='Engagment Days',
            color='Loyalty Classification',
            title='Engagement Days by Loyalty Classification'
        )
        st.plotly_chart(fig_box, use_container_width=True)


    with col2:
        # 8. Chart 3: Loyalty Segments (Pie)
        st.subheader("Loyalty Segments")
        loyalty_counts = df['Loyalty Classification'].value_counts().reset_index()
        loyalty_counts.columns = ['Loyalty Classification', 'Count']
        
        fig_loyalty = px.pie(
            loyalty_counts,
            names='Loyalty Classification',
            values='Count',
            title='Distribution of Client Loyalty'
        )
        st.plotly_chart(fig_loyalty, use_container_width=True)
        
        # 9. Chart 4: Loan by Risk (Bar)
        st.subheader("Total Loan by Risk Weighting")
        # We group by risk and SUM the total loan for each category.
        risk_loans = df.groupby('Risk Weighting')['Total Loan'].sum().reset_index()
        
        fig_risk_loan = px.bar(
            risk_loans,
            x='Risk Weighting',
            y='Total Loan',
            color='Risk Weighting',
            title='Total Loan Amount by Risk Weighting'
        )
        st.plotly_chart(fig_risk_loan, use_container_width=True)

else:
    st.warning("Data could not be loaded. Please check your data files.")