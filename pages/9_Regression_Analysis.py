import streamlit as st
import pandas as pd
import plotly.express as px
from scipy import stats # Import for statistical calculations

# 1. IMPORT OUR CLEANING FUNCTION
from data_processing import load_and_clean_data

# 2. SET PAGE CONFIGURATION
st.set_page_config(page_title="Regression Analysis", page_icon="📈", layout="wide")

# 3. LOAD THE DATA
df = load_and_clean_data()

if not df.empty:
    st.title("Regression Analysis")
    st.markdown("Analyze the statistical relationship between two numerical variables.")

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
        'Bank Loans', 
        'Bank Deposits'
    ]

    # 5. USER SELECTION
    # Create two columns for the dropdown menus
    col1, col2 = st.columns(2)
    with col1:
        x_var = st.selectbox(
            "Select the 'X' Variable (Independent):",
            options=numerical_cols,
            index=0 # Default to 'Estimated Income'
        )
    with col2:
        y_var = st.selectbox(
            "Select the 'Y' Variable (Dependent):",
            options=numerical_cols,
            index=1 # Default to 'Total Deposit'
        )
    
    st.markdown("---")

    if x_var == y_var:
        st.warning("Please select two different variables for the analysis.")
    else:
        # 6. PERFORM STATISTICAL MODELING
        
        # We sample 1000 clients for performance, as plotting all 40k+ is slow
        df_sample = df.sample(min(1000, len(df)))
        
        # Use scipy.stats.linregress to get all regression results
        # We must drop any NaN values for the model to work
        df_clean = df_sample.dropna(subset=[x_var, y_var])
        
        # Calculate the linear regression
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            df_clean[x_var], 
            df_clean[y_var]
        )
        
        # Calculate R-squared
        r_squared = r_value**2
        
        # 7. DISPLAY PLOT
        st.subheader(f"Scatter Plot: {x_var} vs. {y_var}")
        
        # Create a scatter plot with a built-in regression line
        fig_scatter = px.scatter(
            df_clean,
            x=x_var,
            y=y_var,
            title=f"Relationship between {x_var} and {y_var}",
            trendline="ols" # "ols" stands for Ordinary Least Squares (our regression)
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

        # 8. DISPLAY STATISTICAL RESULTS
        st.subheader("Statistical Model Results")
        
        # Display the key metrics in columns
        stat_col1, stat_col2, stat_col3 = st.columns(3)
        with stat_col1:
            st.metric(label="R-squared (R²)", value=f"{r_squared:,.4f}")
        with stat_col2:
            st.metric(label="P-value", value=f"{p_value:,.4f}")
        with stat_col3:
            st.metric(label="Slope", value=f"{slope:,.4f}")
        
        # Explain the results
        st.markdown(f"**Regression Equation:**")
        st.code(f"{y_var} = {slope:,.2f} * {x_var} + {intercept:,.2f}", language="text")
        
        st.markdown(f"**Interpretation:**")
        st.write(f"- **R-squared (R²):** {r_squared*100:,.1f}% of the variance in `{y_var}` can be explained by `{x_var}`.")
        
        if p_value < 0.05:
            st.write(f"- **P-value:** The p-value is {p_value:,.4f} (which is less than 0.05), indicating that the relationship is **statistically significant**.")
        else:
            st.write(f"- **P-value:** The p-value is {p_value:,.4f} (which is greater than 0.05), indicating that the relationship is **not statistically significant**.")

else:
    st.warning("Data could not be loaded. Please check your data files.")