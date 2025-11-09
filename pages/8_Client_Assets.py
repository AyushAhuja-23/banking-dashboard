import streamlit as st
import pandas as pd
import plotly.express as px

# 1. IMPORT OUR CLEANING FUNCTION
from data_processing import load_and_clean_data

# 2. SET PAGE CONFIGURATION
st.set_page_config(page_title="Client Asset Analysis", page_icon="🏠", layout="wide")

# 3. LOAD THE DATA
df = load_and_clean_data()

# 4. SAFETY CHECK
if not df.empty:
    st.title("Client Asset Analysis")
    st.markdown("Analyze client wealth profiles, including properties and savings.")

    # 5. PAGE LAYOUT
    col1, col2 = st.columns(2)

    with col1:
        # 6. Chart 1: Properties Owned (Bar)
        st.subheader("Client Properties Owned")
        # .value_counts() is perfect for categorical numbers like this.
        prop_counts = df['Properties Owned'].value_counts().reset_index()
        prop_counts.columns = ['Properties Owned', 'Client Count']
        
        fig_prop = px.bar(
            prop_counts,
            x='Properties Owned',
            y='Client Count',
            title='Number of Properties Owned by Clients'
        )
        st.plotly_chart(fig_prop, use_container_width=True)

        # 7. Chart 2: Income vs. Savings (Scatter)
        st.subheader("Income vs. Superannuation Savings")
        # We sample 1000 clients for performance
        df_sample = df.sample(min(1000, len(df)))
        
        fig_scatter = px.scatter(
            df_sample,
            x='Estimated Income',
            y='Superannuation Savings',
            color='Loyalty Classification', # Add a color dimension
            title='Estimated Income vs. Superannuation Savings (Sampled)'
        )
        st.plotly_chart(fig_scatter, use_container_width=True)


    with col2:
        # 8. Chart 3: Superannuation Savings (Histogram)
        st.subheader("Superannuation Savings Distribution")
        # A histogram shows the distribution of a continuous number.
        fig_super = px.histogram(
            df,
            x='Superannuation Savings',
            nbins=50, # Use 50 bins
            title='Distribution of Superannuation Savings'
        )
        st.plotly_chart(fig_super, use_container_width=True)

        # 9. Chart 4: Assets by Loyalty (Box Plot)
        st.subheader("Savings by Loyalty")
        # A box plot compares the distributions
        fig_box = px.box(
            df,
            x='Loyalty Classification',
            y='Superannuation Savings',
            color='Loyalty Classification',
            title='Superannuation Savings by Loyalty'
        )
        st.plotly_chart(fig_box, use_container_width=True)

else:
    st.warning("Data could not be loaded. Please check your data files.")