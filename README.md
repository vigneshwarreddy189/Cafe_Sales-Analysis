#  Cafe Sales Data Cleaning & Analysis Project

##  Project Overview

This project focuses on **data cleaning, preprocessing, and sales analysis** of a Cafe Sales dataset using **Python (Pandas, NumPy, Matplotlib)**.

The dataset contained missing values, incorrect entries such as "ERROR" and "UNKNOWN", and inconsistent data types.

## The main goal of this project is to:

1.  Clean and standardize raw sales data
2.  Handle missing and incorrect values
3.  Perform correlation analysis
4. Generate business insights
5. Visualize monthly revenue, top-selling items, and payment methods

##  Technologies Used
1. Python
2. Pandas
3. NumPy
4. Matplotlib
5. Datetime

## Dataset
 File: cafe_sales.csv
 Columns included:

1. transaction_date
2. item
3. quantity
4. price_per_unit_($)
5. total_spent_($)
6. payment_method
7. location

##  Data Cleaning Steps

###  Standardized Column Names

1. Removed spaces
2. Converted to lowercase
3. Replaced spaces with underscores

###  Handled Incorrect Entries

1. Replaced "ERROR" and "UNKNOWN" with:
2. '0' for numeric columns
3. "Unknown" for categorical columns

###  Data Type Conversion

 Converted:

  1. Quantity → Numeric
  2. Price → Float
  3. Total Spent → Float
  4. Transaction Date → Datetime

###  Filled Missing Values

1. Calculated missing quantity using:

  quantity = total_spent / price_per_unit
  

2.  Calculated missing price_per_unit using:

  price_per_unit = total_spent / quantity
  

3.  Calculated missing total_spent using:

  total_spent = quantity × price_per_unit
  

4. Used forward fill (ffill) for missing transaction dates

##  Analysis Performed

###  Correlation Analysis

Calculated correlation between:

1. Quantity
2. Price per unit
3. Total spent

###  Monthly Revenue Trend

Grouped data by month and plotted total revenue.

Insight: Identified peak and low revenue months for better business planning.


###  Top 10 Selling Items

Bar chart visualization of most sold items.

 Insight: Helps identify best-performing products for promotions.
 
###  Payment Method Distribution

Pie chart analysis of:

1. Cash
2. Credit Card
3. Digital Wallet
4. Unknown

 Insight: Understand customer payment preferences.

##  Business Insights & Strategies

Based on analysis:

1. Optimize Peak Periods
   Increase staffing and promotions during high-sales months.

2. Promote Best-Selling Items
   Highlight top-selling items in menu and loyalty programs.

3. Introduce Bundles
   Example: Sandwich + Juice combo to increase transaction value.

4. Improve Low-Performing Items
   Modify recipe, offer discounts, or remove poor-selling items.

5. Seasonal Promotions
   Promote smoothies in summer, hot drinks in winter.

##  Project Outcome

1. Cleaned and structured dataset
2. Improved data quality
3. Identified sales trends
4. Generated actionable business insights
5. Created visual reports

##  Author

Vigneshwar Reddy
MBA | Aspiring Data Analyst
Skilled in Excel, Python, SQL, Tableau

