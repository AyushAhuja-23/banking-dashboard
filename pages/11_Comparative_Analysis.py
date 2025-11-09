import streamlit as st
import pandas as pd
import plotly.express as px
from scipy import stats # Import for statistical tests

# 1. IMPORT OUR CLEANING FUNCTION
from data_processing import load_and_clean_data

# 2. SET PAGE CONFIGURATION
st.set_page_config(page_title="Comparative Analysis", page_icon="📊", layout="wide")

# 3. LOAD THE DATA
df = load_and_clean_data()

if not df.empty:
    st.title("Comparative Analysis (T-tests & ANOVA)")
    st.markdown("Test if the difference between client groups is statistically significant.")

    # 4. DEFINE VARIABLE LISTS
    # We need one list for categories and one for numbers.
    categorical_cols = [
        'Gender', 
        'Loyalty Classification', 
        'Income Band', 
        'Banking Relationship', 
        'Risk Weighting',
        'Occupation',
        'Nationality'
    ]
    numerical_cols = [
        'Estimated Income', 
        'Total Deposit', 
        'Total Loan', 
        'Age', 
        'Engagment Days', 
        'Superannuation Savings',
        'Bank Loans', 
        'Bank Deposits'
    ]

    # 5. USER SELECTION
    st.subheader("Select Variables to Compare")
    col1, col2 = st.columns(2)
    with col1:
        cat_var = st.selectbox(
            "Select the Categorical Group (e.g., Gender):",
            options=categorical_cols,
            index=0 # Default to 'Gender'
        )
    with col2:
        num_var = st.selectbox(
            "Select the Numerical Value (e.g., Total Deposit):",
            options=numerical_cols,
            index=1 # Default to 'Total Deposit'
        )
    
    st.markdown("---")

    # 6. VISUALIZE THE DIFFERENCE
    st.subheader(f"Visual Distribution of {num_var} by {cat_var}")
    
    # A box plot is the best way to visualize this
    fig_box = px.box(
        df.dropna(subset=[cat_var, num_var]), # Drop NaNs for plotting
        x=cat_var,
        y=num_var,
        color=cat_var,
        title=f"{num_var} Distribution by {cat_var}"
    )
    # If we have too many categories (like Occupation), hide the x-axis labels
    if df[cat_var].nunique() > 10:
        fig_box.update_xaxes(showticklabels=False)
        
    st.plotly_chart(fig_box, use_container_width=True)
    
    # 7. PERFORM STATISTICAL MODELING
    
    # Get all unique groups from the selected category
    groups = df[cat_var].dropna().unique()
    
    # Create a list of data arrays, one for each group
    group_data = []
    for group in groups:
        group_data.append(df[df[cat_var] == group][num_var].dropna())

    # --- Run the correct test based on the number of groups ---
    
    st.subheader("Statistical Model Results")
    stat_col1, stat_col2, stat_col3 = st.columns(3)
    
    if len(group_data) == 2:
        # --- T-Test (2 groups) ---
        # Unpack the two groups of data
        data1 = group_data[0]
        data2 = group_data[1]
        
        # Run the independent T-test
        t_stat, p_value = stats.ttest_ind(data1, data2, equal_var=False) # 'equal_var=False' is safer
        
        with stat_col1:
            st.metric("Test Performed", "T-test")
        with stat_col2:
            st.metric("T-Statistic", f"{t_stat:,.4f}")
        with stat_col3:
            st.metric("P-value", f"{p_value:,.4f}")

    elif len(group_data) > 2:
        # --- ANOVA (3+ groups) ---
        # The '*' unpacks the list of data arrays for the function
        f_stat, p_value = stats.f_oneway(*group_data)
        
        with stat_col1:
            st.metric("Test Performed", "ANOVA")
        with stat_col2:
            st.metric("F-Statistic", f"{f_stat:,.4f}")
        with stat_col3:
            st.metric("P-value", f"{p_value:,.4f}")
            
    else:
        st.warning(f"The selected variable '{cat_var}' has less than 2 groups. Cannot perform a test.")
        p_value = 1.0 # Set p-value to 1 to show 'not significant'

    # 8. DISPLAY INTERPRETATION
    st.subheader("Interpretation")
    if p_value < 0.05:
        st.success(f"**The result is statistically significant (p < 0.05).**")
        st.write(f"This means there is a very low probability that the observed differences in `{num_var}` between the `{cat_var}` groups are due to random chance. The differences are likely real.")
    else:
        st.error(f"**The result is not statistically significant (p >= 0.05).**")
        st.write(f"This means we cannot conclude that the observed differences in `{num_var}` between the `{cat_var}` groups are real. The differences could simply be due to random chance.")

else:
    st.warning("Data could not be loaded. Please check your data files.")