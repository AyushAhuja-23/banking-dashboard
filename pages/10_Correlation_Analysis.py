import streamlit as st
import pandas as pd
import plotly.express as px

# 1. IMPORT OUR CLEANING FUNCTION
from data_processing import load_and_clean_data

# 2. SET PAGE CONFIGURATION
st.set_page_config(page_title="Correlation Analysis", page_icon="🔗", layout="wide")

# 3. LOAD THE DATA
df = load_and_clean_data()

if not df.empty:
    st.title("Correlation Analysis")
    st.markdown("Analyze the correlation between different numerical features in the dataset.")

    # 4. DEFINE NUMERICAL COLUMNS
    # These are the columns a user can select for the analysis
    numerical_cols = [
        'Estimated Income', 
        'Total Deposit', 
        'Total Loan', 
        'Age', 
        'Engagment Days', 
        'Superannuation Savings', 
        'Properties Owned',
        'Amount of Credit Cards',
        'Credit Card Balance',
        'Bank Loans', 
        'Bank Deposits',
        'Checking Accounts',
        'Saving Accounts'
    ]
    
    # 5. USER SELECTION
    st.subheader("Select Variables for Correlation")
    
    # st.multiselect allows the user to pick multiple items from a list
    selected_cols = st.multiselect(
        "Select at least 2 variables to compare:",
        options=numerical_cols,
        default=numerical_cols[:5] # Default to the first 5 columns
    )

    st.markdown("---")

    if len(selected_cols) < 2:
        st.warning("Please select at least two variables to calculate the correlation.")
    else:
        # 6. PERFORM STATISTICAL MODELING
        
        # Select only the columns the user has chosen
        df_selected = df[selected_cols]
        
        # Calculate the correlation matrix
        # .corr() is the pandas function that runs the statistical model
        corr_matrix = df_selected.corr()
        
        # 7. DISPLAY HEATMAP
        st.subheader("Correlation Heatmap")
        
        # Create a heatmap figure using Plotly Express
        # z = the correlation matrix
        # x and y = the column names
        # color_continuous_scale = a nice blue-to-red color scale
        # text_auto=True adds the correlation values on top of the squares
        fig_heatmap = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            color_continuous_scale='RdBu_r', # Red-Blue-Reverse
            zmin=-1, # Force scale from -1
            zmax=1   # to +1
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)

        # 8. DISPLAY CORRELATION TABLE
        st.subheader("Correlation Matrix (Table)")
        st.dataframe(
            corr_matrix.style.background_gradient(cmap='RdBu_r', vmin=-1, vmax=1).format("{:.2f}"),
            use_container_width=True
        )
        
        st.markdown("""
        **How to Read This:**
        * **+1.0 (Dark Blue):** Perfect positive correlation. When one variable goes up, the other goes up.
        * **-1.0 (Dark Red):** Perfect negative correlation. When one variable goes up, the other goes down.
        * **0.0 (White):** No correlation. The variables are not related.
        """)

else:
    st.warning("Data could not be loaded. Please check your data files.")