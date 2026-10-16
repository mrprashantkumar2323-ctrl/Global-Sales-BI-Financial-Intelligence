"""
Global Commercial Sales & RFM Customer Segmentation Pipeline
Author: Prashant Kumar
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def build_sales_intelligence_engine(n_transactions=5000):
    np.random.seed(101)
    
    customers = [f"CUST_{i:04d}" for i in range(1, 501)]
    categories = ['Electronics', 'Accessories', 'Bikes', 'Components', 'Apparel']
    countries = ['United States', 'United Kingdom', 'Germany', 'Australia', 'India']
    
    start_date = datetime(2025, 1, 1)
    dates = [start_date + timedelta(days=int(np.random.exponential(120))) for _ in range(n_transactions)]
    dates = [d for d in dates if d <= datetime(2026, 10, 1)]
    actual_len = len(dates)
    
    df = pd.DataFrame({
        'TransactionID': [f"TXN_{i:06d}" for i in range(1, actual_len + 1)],
        'Date': dates,
        'CustomerID': np.random.choice(customers, actual_len),
        'Category': np.random.choice(categories, actual_len),
        'Country': np.random.choice(countries, actual_len),
        'Quantity': np.random.randint(1, 8, actual_len),
        'UnitPrice': np.random.uniform(25, 1200, actual_len),
        'DiscountRate': np.random.choice([0.0, 0.05, 0.10, 0.15], actual_len, p=[0.5, 0.25, 0.15, 0.10])
    })
    
    df['GrossRevenue'] = df['Quantity'] * df['UnitPrice']
    df['NetRevenue'] = df['GrossRevenue'] * (1 - df['DiscountRate'])
    df['Cost'] = df['NetRevenue'] * np.random.uniform(0.55, 0.75, actual_len)
    df['GrossProfit'] = df['NetRevenue'] - df['Cost']
    
    print("[+] Sales Intelligence Engine Computed:")
    print(f"  Total Net Revenue:  ${df['NetRevenue'].sum():,.2f}")
    print(f"  Total Gross Profit: ${df['GrossProfit'].sum():,.2f}")
    print(f"  Overall Margin:     {(df['GrossProfit'].sum() / df['NetRevenue'].sum()) * 100:.2f}%")
    
    # RFM Segmentation
    snapshot_date = df['Date'].max() + timedelta(days=1)
    rfm = df.groupby('CustomerID').agg({
        'Date': lambda x: (snapshot_date - x.max()).days,
        'TransactionID': 'count',
        'NetRevenue': 'sum'
    }).rename(columns={'Date': 'Recency', 'TransactionID': 'Frequency', 'NetRevenue': 'Monetary'})
    
    print("
[+] Top 5 High-Value Enterprise Customers (RFM):")
    print(rfm.sort_values(by='Monetary', ascending=False).head(5))

if __name__ == '__main__':
    build_sales_intelligence_engine()
