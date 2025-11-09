import pandas as pd
import numpy as np
import streamlit as st

# 1. CACHE THE DATA
# This @st.cache_data decorator tells Streamlit to run this function
# only ONCE. After the first run, it saves the result in memory.
# This makes the app super fast, as we don't reload and clean the
# data every time a user clicks a filter.
@st.cache_data
def load_and_clean_data():
    """
    This is the main function that loads all 4 raw data files, 
    merges them, cleans them, and creates all new features.
    It returns a single, final DataFrame.
    """
    
    # 2. DEFINE FILE NAMES
    file_main = "Banking.csv"
    file_gender = "gender.csv"
    file_relationship = "banking-realtionships.csv"
    file_advisor = "investment-advisiors.csv"
    
    # 3. LOAD RAW DATA
    # A try/except block is used to catch errors if files are missing.
    try:
        df_main = pd.read_csv(file_main)
        df_gender = pd.read_csv(file_gender)
        df_relationship = pd.read_csv(file_relationship)
        df_advisor = pd.read_csv(file_advisor)

        # 4. MERGE DATAFRAMES
        # We merge the 3 small "dimension" tables into the main "fact" table.
        # We use the correct keys we found during our investigation.
        df_merged = df_main.merge(df_gender, on='GenderId', how='left')
        df_merged = df_merged.merge(df_relationship, on='BRId', how='left')
        df_merged = df_merged.merge(df_advisor, on='IAId', how='left')

        # 5. CLEAN & TRANSFORM (FEATURE ENGINEERING)
        
        # 5a. Clean Financial Columns
        # This loop finds any missing values (NaNs) in the financial columns
        # and replaces them with 0, so we can do math without errors.
        financial_cols = [
            'Bank Loans', 'Business Lending', 'Credit Card Balance', 
            'Bank Deposits', 'Saving Accounts', 'Foreign Currency Account', 'Checking Accounts'
        ]
        for col in financial_cols:
            df_merged[col] = pd.to_numeric(df_merged[col], errors='coerce').fillna(0)

        # 5b. Create 'Engagment Days'
        df_merged['Joined Bank'] = pd.to_datetime(df_merged['Joined Bank'], errors='coerce')
        df_merged['Engagment Days'] = (pd.Timestamp.today() - df_merged['Joined Bank']).dt.days

        # 5c. Create 'Engagement Timeframe' (Binning)
        # We use pd.cut to group the 'Engagment Days' into categories.
        bins_time = [-float('inf'), 365, 1825, 3650, 7300, float('inf')]
        labels_time = ["< 1 Years", "< 5 Years", "< 10 Years", "< 20 Years", "> 20 Years"]
        df_merged['Engagement Timeframe'] = pd.cut(df_merged['Engagment Days'], bins=bins_time, labels=labels_time, right=False)

        # 5d. Create 'Income Band' (Binning)
        # Same logic, but for 'Estimated Income'.
        df_merged['Estimated Income'] = pd.to_numeric(df_merged['Estimated Income'], errors='coerce').fillna(0)
        bins_income = [-float('inf'), 100000, 300000, float('inf')]
        labels_income = ["Low", "Mid", "High"]
        df_merged['Income Band'] = pd.cut(df_merged['Estimated Income'], bins=bins_income, labels=labels_income, right=False)

        # 5e. Create 'Processing Fees' (Mapping)
        # We use .map() to convert text categories into numbers.
        fee_map = { "High": 0.05, "Mid": 0.03, "Low": 0.01 }
        df_merged['Processing Fees'] = df_merged['Fee Structure'].map(fee_map).fillna(0)

        # 5f. Create 'Total Loan'
        df_merged['Total Loan'] = df_merged['Bank Loans'] + df_merged['Business Lending'] + df_merged['Credit Card Balance']

        # 5g. Create 'Total Deposit'
        df_merged['Total Deposit'] = df_merged['Bank Deposits'] + df_merged['Saving Accounts'] + \
                                     df_merged['Foreign Currency Account'] + df_merged['Checking Accounts']
                                     
        # 6. FINALIZE & RETURN
        # We drop the old ID columns since we now have the text names (e.g., "Male", "Private Bank").
        cols_to_drop = ['GenderId', 'BRId', 'IAId']
        df_final = df_merged.drop(columns=cols_to_drop)
        
        # This is the final, clean DataFrame that all our app pages will use.
        return df_final
    
    except FileNotFoundError as e:
        # If a file is missing, show an error on the app.
        st.error(f"Error: {e}. One of the 4 data files was not found.")
        return pd.DataFrame() # Return an empty DataFrame
    except KeyError as e:
        # If a merge key is wrong, show an error.
        st.error(f"KeyError: {e}. A column name for merging is incorrect.")
        return pd.DataFrame() # Return an empty DataFrame