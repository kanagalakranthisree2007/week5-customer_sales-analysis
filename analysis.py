import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load datasets
sales_data = pd.read_csv(r"C:\Users\kanag\OneDrive\Desktop\intenship\customer_sales_analysis\data\sales_data.csv")
churn_data = pd.read_csv(r"C:\Users\kanag\OneDrive\Desktop\intenship\customer_sales_analysis\data\customer_churn.csv")

# Explore data
print(sales_data.head())
print(sales_data.info())
print(sales_data.describe())
print(sales_data.isnull().sum())

# Clean data
sales_data = sales_data.dropna()
sales_data['Date'] = pd.to_datetime(sales_data['Date'])
sales_data['Total'] = sales_data['Quantity'] * sales_data['Price']

print(sales_data.head())

# Check actual column names
print("Columns in sales_data:", sales_data.columns)

# Replace with correct column name from your dataset
# Example: if you see 'CustID' or 'Customer_Name', use that instead of 'CustomerID'
customer_col = 'CustomerID'   # CHANGE this to match your dataset

# Customer analysis
if customer_col in sales_data.columns:
    customer_sales = sales_data.groupby(customer_col)['Total'].sum().reset_index()
    top_customers = customer_sales.nlargest(10, 'Total')
    print(top_customers)

# Regional distribution
if 'Region' in sales_data.columns:
    region_sales = sales_data.groupby('Region')['Total'].sum().reset_index()
    print(region_sales)

# Monthly sales
sales_data['Month'] = sales_data['Date'].dt.month
monthly_sales = sales_data.groupby('Month')['Total'].sum().reset_index()
print(monthly_sales)

# Product analysis
if 'Product' in sales_data.columns:
    product_sales = sales_data.groupby('Product')['Total'].sum().reset_index().nlargest(10, 'Total')
    print(product_sales)

# Pivot table (Region vs Product)
if 'Region' in sales_data.columns and 'Product' in sales_data.columns:
    pivot = pd.pivot_table(sales_data, values='Total', index='Region', columns='Product', aggfunc='sum', fill_value=0)
    print(pivot)

# Visualizations
plt.figure(figsize=(10,6))
sns.lineplot(data=monthly_sales, x='Month', y='Total')
plt.title("Monthly Revenue Trend")
plt.show()

if customer_col in sales_data.columns:
    plt.figure(figsize=(10,6))
    sns.barplot(data=top_customers, x=customer_col, y='Total')
    plt.title("Top Customers by Revenue")
    plt.xticks(rotation=45)
    plt.show()

if 'Region' in sales_data.columns:
    plt.figure(figsize=(8,6))
    plt.pie(region_sales['Total'], labels=region_sales['Region'], autopct='%1.1f%%')
    plt.title("Regional Sales Distribution")
    plt.show()

# Report & Insights
total_revenue = sales_data['Total'].sum()
if customer_col in sales_data.columns:
    total_customers = sales_data[customer_col].nunique()
else:
    total_customers = "Column not found"

avg_order_value = sales_data['Total'].mean()

print("CUSTOMER SALES ANALYSIS REPORT")
print(f"Total Revenue: ${total_revenue}")
print(f"Total Customers: {total_customers}")
print(f"Average Order Value: ${avg_order_value}")

if customer_col in sales_data.columns:
    top_customer = top_customers.iloc[0]
    print(f"Top Customer: {top_customer[customer_col]} - ${top_customer['Total']}")
