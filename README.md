\# Interactive Banking Dashboard



This is a multi-page interactive dashboard for banking analysis, built with Python \& Streamlit. This project ingests, cleans, and merges multiple raw data files to create a 16-page application for advanced data analysis and data mining.



\## 🚀 Features



\* \*\*16 Unique Pages:\*\* A full-featured app covering everything from high-level KPIs to advanced statistical modeling.

\* \*\*Data Processing Pipeline:\*\* A single, cached function (`data\_processing.py`) that loads, merges, cleans, and "feature-engineers" all data.

\* \*\*Advanced Analytics:\*\* Includes pages for:

&nbsp;   \* Regression Analysis (Scipy)

&nbsp;   \* Correlation Analysis (Heatmaps)

&nbsp;   \* Comparative Analysis (T-tests \& ANOVA)

&nbsp;   \* Time Series \& Cohort Analysis

\* \*\*Data Mining:\*\*

&nbsp;   \* \*\*Product Affinity (Association Rules):\*\* Uses `mlxtend` to find "if-then" rules for cross-selling products.

\* \*\*Management Tools:\*\*

&nbsp;   \* Client Drill-Down

&nbsp;   \* Advisor Performance Leaderboards

&nbsp;   \* Risk \& Loyalty Analysis

&nbsp;   \* Product Penetration \& Cross-Sell Finder



\## 🛠️ Technology Stack



\* \*\*Streamlit:\*\* Core web app framework.

\* \*\*Pandas:\*\* For all data manipulation.

\* \*\*Plotly Express:\*\* For interactive visualizations.

\* \*\*Scipy:\*\* For statistical models (Regression, T-test, ANOVA).

\* \*\*Mlxtend:\*\* For data mining (Association Rules).



\## 🏃 How to Run



1\.  Clone this repository.

2\.  Install the required libraries:

&nbsp;   ```bash

&nbsp;   pip install -r requirements.txt

&nbsp;   ```

3\.  Place the required raw data files in the main folder (e.g., `Banking.csv`, `gender.csv`, etc.).

4\.  Run the app from your terminal:

&nbsp;   ```bash

&nbsp;   streamlit run 1\_Home.py

&nbsp;   ```

