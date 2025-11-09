import streamlit as st
import pandas as pd
import plotly.express as px

# 1. IMPORT OUR CLEANING FUNCTION
from data_processing import load_and_clean_data

# 2. SET PAGE CONFIGURATION
st.set_page_config(page_title="Client Demographics", page_icon="👥", layout="wide")

# 3. LOAD THE DATA
df = load_and_clean_data()

# 4. SAFETY CHECK
if not df.empty:
    st.title("Client Demographics")
    st.markdown("Analyze the bank's customer base by age, nationality, occupation, and income.")

    # 5. PAGE LAYOUT
    col1, col2 = st.columns(2)

    with col1:
        # 6. Chart 1: Age Distribution (Histogram)
        st.subheader("Age Distribution of Clients")
        # A histogram is perfect for showing the distribution of a single number.
        fig_age = px.histogram(
            df, 
            x='Age', 
            nbins=20, # We group ages into 20 bins
            title='Client Age Distribution'
        )
        st.plotly_chart(fig_age, use_container_width=True)

        # 7. Chart 2: Top Occupations (Bar)
        st.subheader("Top Client Occupations")
        # .value_counts() gets the counts for each occupation
        # .nlargest(15) selects only the top 15
        top_occupations = df['Occupation'].value_counts().nlargest(15).reset_index()
        top_occupations.columns = ['Occupation', 'Count']
        
        fig_occ = px.bar(
            top_occupations, 
            y='Occupation', # y is categorical
            x='Count',      # x is numerical
            orientation='h', # This makes it a horizontal bar chart
            title='Top 15 Client Occupations'
        )
        st.plotly_chart(fig_occ, use_container_width=True)

    with col2:
        # 8. Chart 3: Nationality (Pie)
        st.subheader("Nationality Breakdown")
        top_nationalities = df['Nationality'].value_counts().nlargest(15).reset_index()
        top_nationalities.columns = ['Nationality', 'Count']

        fig_nat = px.pie(
            top_nationalities,
            names='Nationality',
            values='Count',
            title='Top 15 Client Nationalities'
        )
        st.plotly_chart(fig_nat, use_container_width=True)
        
        # 9. Chart 4: Income vs. Age (Scatter)
        st.subheader("Income vs. Age")
        # Plotting 40,000+ dots is slow. We take a random sample
        # of 1000 dots to make the chart fast and responsive.
        df_sample = df.sample(min(1000, len(df)))
        fig_scatter = px.scatter(
            df_sample,
            x='Age',
            y='Estimated Income',
            color='Gender', # We can use color to add a 3rd dimension
            title='Estimated Income vs. Age (Sampled)'
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

else:
    st.warning("Data could not be loaded. Please check your data files.")