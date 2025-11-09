import streamlit as st
import pandas as pd
import numpy as np # Import numpy
from mlxtend.frequent_patterns import apriori, association_rules

# 1. IMPORT OUR CLEANING FUNCTION
from data_processing import load_and_clean_data

# 2. SET PAGE CONFIGURATION
st.set_page_config(page_title="Product Affinity", page_icon="🛒", layout="wide")

# 3. LOAD THE DATA
df = load_and_clean_data()

# 4. DEFINE PRODUCT COLUMNS
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
    st.title("Product Affinity (Association Rules)")
    st.markdown("Discover which products are most frequently held together by clients.")

    # 6. DATA BINARIZATION
    df_basket = pd.DataFrame()
    for col in product_cols:
        df_basket[col] = (df[col] > 0).astype(bool) 

    st.subheader("Client Product Holdings (Sample)")
    st.dataframe(df_basket.head(), use_container_width=True)
    st.markdown("---")
    
    # 7. USER-CONTROLLED THRESHOLD
    st.subheader("Data Mining Model Controls")
    min_support_slider = st.slider(
        "Select Minimum Support Threshold:",
        min_value=0.01, max_value=0.1, value=0.02, step=0.01,
        format="%.2f (%.0f%%)"
    )

    # 8. RUN DATA MINING MODELS
    try:
        frequent_itemsets = apriori(
            df_basket, 
            min_support=min_support_slider, 
            use_colnames=True
        )

        # --- NEW CODE: Suppress the RuntimeWarning ---
        # We wrap the calculation in 'np.errstate' to
        # temporarily ignore 'invalid divide' warnings.
        with np.errstate(divide='ignore', invalid='ignore'):
            rules = association_rules(
                frequent_itemsets, 
                metric="lift", 
                min_threshold=1.0 
            )
        # --- End of new code ---
            
        rules = rules.sort_values(by='confidence', ascending=False)
        
        st.markdown("---")
        st.subheader("Top Association Rules")

        # 9. DISPLAY RESULTS
        if rules.empty or rules.shape[0] == 0:
            st.warning("No association rules found with the current settings. Try lowering the 'Minimum Support Threshold'.")
        else:
            rules_display = rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].copy()
            
            rules_display['antecedents'] = rules_display['antecedents'].apply(lambda x: ', '.join(list(x)))
            rules_display['consequents'] = rules_display['consequents'].apply(lambda x: ', '.join(list(x)))
            
            st.dataframe(
                rules_display.style
                .format({
                    'support': '{:.2%}',
                    'confidence': '{:.2%}',
                    'lift': '{:.2f}'
                }),
                use_container_width=True
            )

            st.markdown("""
            **How to Read This Table:**
            * **antecedents:** The product(s) a client already has.
            * **consequents:** The product(s) the client is likely to get.
            * **support:** Percentage of *all clients* who have both.
            * **confidence:** "If a client has the **antecedent**, what is the % chance they also have the **consequent**?"
            * **lift:** How much more likely a client is to get the consequent (vs. a random client). **A lift > 1 is a strong signal.**
            """)

    except Exception as e:
        st.error(f"An error occurred during mining. This can happen if the support threshold is too low for the data.")
        st.exception(e)

else:
    st.warning("Data could not be loaded. Please check your data files.")