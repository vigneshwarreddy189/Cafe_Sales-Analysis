import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Load the CSV file
df = pd.read_csv("C:/Users/tammi/Desktop/cafe_sales.csv")

# Standardize column names
df.columns = df.columns.str.strip().str.replace(' ', '_').str.lower()

# --- Data Cleaning ---

# 1. Handle missing values and incorrect entries ("ERROR", "UNKNOWN")
# Replace "ERROR" and "UNKNOWN" with 0 for numeric columns
numeric_columns = ['quantity', 'price_per_unit_($)', 'total_spent_($)']
for col in numeric_columns:
    df[col] = df[col].replace(['ERROR', 'UNKNOWN'], 0)
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)  # Coerce remaining invalid to 0

# Replace missing or "ERROR"/"UNKNOWN" in item, payment_method, location with "Unknown"
df['item'] = df['item'].replace(['ERROR', 'UNKNOWN'], 'Unknown').fillna('Unknown').str.title()
df['payment_method'] = df['payment_method'].replace(['ERROR', 'UNKNOWN'], 'Unknown').fillna('Unknown').str.title()
df['location'] = df['location'].replace(['ERROR', 'UNKNOWN'], 'Unknown').fillna('Unknown').str.title()

# Convert transaction_id to string
df['transaction_id'] = df['transaction_id'].astype(str)

# Convert transaction_date to datetime, impute missing with median date
df['transaction_date'] = pd.to_datetime(df['transaction_date'], errors='coerce')
median_date = df['transaction_date'].median()
df['transaction_date'] = df['transaction_date'].fillna(median_date)

# 2. Validate and correct total_spent_($)
df['expected_total'] = df['quantity'] * df['price_per_unit_($)']
df['total_spent_($)'] = np.where(
    (df['total_spent_($)'] == 0) | 
    (abs(df['total_spent_($)'] - df['expected_total']) > 0.01),
    df['expected_total'],
    df['total_spent_($)']
)
df = df.drop('expected_total', axis=1)

# 3. Convert data types
df['quantity'] = df['quantity'].astype(int)  # Quantities are whole numbers
df['price_per_unit_($)'] = df['price_per_unit_($)'].astype(float)
df['total_spent_($)'] = df['total_spent_($)'].astype(float)
df['item'] = df['item'].astype(str)
df['payment_method'] = df['payment_method'].astype(str)
df['location'] = df['location'].astype(str)

# 4. Remove duplicates based on transaction_id
df = df.drop_duplicates(subset=['transaction_id'], keep='first')

# 5. Ensure positive quantities and non-negative prices
df = df[(df['quantity'] > 0) & (df['price_per_unit_($)'] >= 0) & (df['total_spent_($)'] >= 0)]

# Reset index
df = df.reset_index(drop=True)

# Save cleaned dataset
df.to_csv('cleaned_cafe_sales.csv', index=False)

# --- Correlation Analysis ---
# Select numeric columns for correlation
numeric_cols = ['quantity', 'price_per_unit_($)', 'total_spent_($)']
correlation_matrix = df[numeric_cols].corr()


# --- Insights and Strategy ---
# 1. Peak Sales Periods
df['month'] = df['transaction_date'].dt.month
df['day_of_week'] = df['transaction_date'].dt.day_name()
monthly_sales = df.groupby('month')['total_spent_($)'].sum()
day_sales = df.groupby('day_of_week')['total_spent_($)'].sum()

# Plot monthly sales
plt.figure(figsize=(10, 6))
plt.bar(range(1, 13), monthly_sales, color='skyblue')
plt.title('Total Sales by Month')
plt.xlabel('Month')
plt.ylabel('Total Revenue ($)')
plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.savefig('monthly_sales.png')
plt.close()

# Plot sales by day of week
plt.figure(figsize=(10, 6))
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day_sales = day_sales.reindex(days)
plt.bar(days, day_sales, color='lightgreen')
plt.title('Total Sales by Day of Week')
plt.xlabel('Day of Week')
plt.ylabel('Total Revenue ($)')
plt.xticks(rotation=45)
plt.savefig('day_sales.png')
plt.close()

# 2. Best-Selling Items
item_sales = df.groupby('item')['total_spent_($)'].sum().sort_values(ascending=False)
item_quantity = df.groupby('item')['quantity'].sum().sort_values(ascending=False)

# Plot top-selling items by revenue
plt.figure(figsize=(10, 6))
top_items = item_sales.head(10)
plt.bar(top_items.index, top_items, color='coral')
plt.title('Top 10 Items by Revenue')
plt.xlabel('Item')
plt.ylabel('Total Revenue ($)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('top_items_revenue.png')
plt.close()

# 3. Revenue Trends
df['date'] = df['transaction_date'].dt.to_period('M')
revenue_trend = df.groupby('date')['total_spent_($)'].sum()

# Plot revenue trend
plt.figure(figsize=(12, 6))
plt.plot(revenue_trend.index.astype(str), revenue_trend, marker='o', color='purple')
plt.title('Monthly Revenue Trend (2023)')
plt.xlabel('Month')
plt.ylabel('Total Revenue ($)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('revenue_trend.png')
plt.close()

# --- Print Summary ---
print("Cleaned Data Summary:")
print(df.info())
print("\nMissing Values After Cleaning:")
print(df.isna().sum())
print("\nCorrelation Matrix:")
print(correlation_matrix)

print("\nTop 5 Best-Selling Items by Revenue:")
print(item_sales.head())
print("\nTop 5 Best-Selling Items by Quantity:")
print(item_quantity.head())
print("\nPeak Sales Months:")
print(monthly_sales.sort_values(ascending=False).head())
print("\nPeak Sales Days of Week:")
print(day_sales.sort_values(ascending=False).head())

# --- Strategies to Improve Sales and Revenue ---
print("\nStrategies to Improve Sales and Revenue:")
print("1. **Optimize Peak Periods**: Increase staffing and promotions during high-sales months and days (e.g., busiest days identified in the analysis). Offer discounts during low-sales periods to boost demand.")
print("2. **Promote Best-Selling Items**: Focus marketing on top items (e.g., Sandwiches, Smoothies) through menu highlights or loyalty programs.")
print("3. **Introduce Bundles**: Create combo deals with high-revenue items (e.g., Sandwich + Juice) to increase average transaction value.")
print("4. **Target Low-Performing Items**: For items with low sales (e.g., Tea), consider recipe enhancements, promotions, or removal from the menu.")
print("5. **Enhance Payment Methods**: If Digital Wallet or Credit Card usage is high, streamline these payment options to improve customer experience.")
print("6. **Seasonal Promotions**: Align offerings with seasonal trends (e.g., smoothies in summer, hot drinks in winter) based on monthly sales patterns.")
print("7. **Reduce Waste**: Use historical sales data for demand forecasting to optimize inventory, especially for perishable items like Salads and Cakes.")
