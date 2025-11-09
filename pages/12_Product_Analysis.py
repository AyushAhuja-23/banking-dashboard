import streamlit as st
import pandas as pd
import plotly.express as px

# 1. IMPORT OUR CLEANING FUNCTION
from data_processing import load_and_clean_data

# 2. SET PAGE CONFIGURATION
st.set_page_config(page_title="Product Analysis", page_icon="🎁", layout="wide")

# 3. LOAD THE DATA
df = load_and_clean_data()

# 4. DEFINE PRODUCT COLUMNS
# These are the columns we'll analyze as "products"
product_cols = [
    'Bank Loans', 
    'Business Lending', 
    'Credit Card Balance', 
    'Saving Accounts', 
    'Checking Accounts', 
    'Foreign Currency Account'
]

# 5. SAFETY CHECK
if not df.empty:
    st.title("Product Penetration & Cross-Sell Analysis")

    # --- 6. Feature 1: Product Penetration ---
    st.subheader("Product Penetration")
    st.markdown("What percentage of all clients have each product?")

    # Calculate penetration
    total_clients = len(df)
    penetration_data = []

    for col in product_cols:
        # A client "has" a product if the value is greater than 0
        clients_with_product = df[df[col] > 0].shape[0]
        percentage = (clients_with_product / total_clients)
        penetration_data.append({
            'Product': col.replace('_', ' '), # Clean up name
            'Percentage': percentage,
            'Client Count': clients_with_product
        })
    
    # Create a DataFrame from our calculated data
    df_penetration = pd.DataFrame(penetration_data).sort_values(by='Percentage', ascending=False)

    # Create the Bar Chart
    fig_pen = px.bar(
        df_penetration,
        x='Product',
        y='Percentage',
        text=df_penetration['Percentage'].apply(lambda x: f'{x:.1%}'), # Format text as %
        title='Product Penetration (% of Total Clients)'
    )
    fig_pen.update_layout(yaxis_tickformat=".0%")
    st.plotly_chart(fig_pen, use_container_width=True)

    st.markdown("---")

    # --- 7. Feature 2: Cross-Sell Opportunity Finder ---
    st.subheader("Cross-Sell Opportunity Finder")
    st.markdown("Find clients who have certain products but *not* others.")

    # Create two columns for the filters
    col1, col2 = st.columns(2)

    with col1:
        # Filter 1: Clients who HAVE...
        have_products = st.multiselect(
            "Find clients who HAVE these products:",
            options=product_cols,
            default=[product_cols[3]] # Default to 'Saving Accounts'
        )

    with col2:
        # Filter 2: Clients who do NOT HAVE...
        not_have_products = st.multiselect(
            "And do NOT HAVE these products:",
            options=product_cols,
            default=[product_cols[2]] # Default to 'Credit Card Balance'
        )

    # 8. FILTERING LOGIC
    # Start with all clients
    df_filtered = df.copy()

    # Apply the "HAVE" filter
    if have_products:
        for product in have_products:
            df_filtered = df_filtered[df_filtered[product] > 0]

    # Apply the "NOT HAVE" filter
    if not_have_products:
        for product in not_have_products:
            df_filtered = df_filtered[df_filtered[product] == 0]

    # 9. DISPLAY RESULTS
    st.metric(
        label="Target Clients Found",
        value=f"{df_filtered.shape[0]:,} clients"
    )

    # Define which columns to show in the final table
    display_cols = [
        'Client ID', 
        'Name', 
        'Occupation', 
        'Estimated Income', 
        'Investment Advisor', 
        'Loyalty Classification', 
        'Engagment Days'
    ]
    
    # Add the selected product columns to the table so the user can verify
    display_cols = display_cols + have_products + not_have_products
    # Remove duplicates if any
    display_cols = list(dict.fromkeys(display_cols)) 

    st.dataframe(df_filtered[display_cols], use_container_width=True)

else:
    st.warning("Data could not be loaded. Please check your data files.")