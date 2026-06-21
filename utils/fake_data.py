import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_demo_db():
    np.random.seed(42)
    dates = pd.date_range('2022-01-01', '2023-12-31', freq='D')
    products = ['Laptop', 'Phone', 'Tablet', 'Monitor']
    regions = ['EU', 'US', 'ASIA']
    data = []
    for date in dates:
        for product in products:
            for region in regions:
                qty = np.random.randint(0, 20)
                price = np.random.choice([1500, 800, 600, 300]) if product == 'Laptop' else \
                        np.random.choice([700, 400, 200, 150]) if product == 'Phone' else \
                        np.random.choice([500, 300, 100, 80])
                data.append([date.strftime('%Y-%m-%d'), product, region, qty, price, qty*price])
    df = pd.DataFrame(data, columns=['Date', 'Product', 'Region', 'Quantity', 'UnitPrice', 'Sales'])
    df['CustomerID'] = np.random.randint(1000, 1020, size=len(df))
    dim_customer = pd.DataFrame({
        'CustomerID': range(1000, 1020),
        'CustomerName': ['Customer_' + str(i) for i in range(1000,1020)],
        'Country': np.random.choice(['Germany', 'USA', 'Japan', 'UK'], 20)
    })
    conn = sqlite3.connect('sales.db')
    df.to_sql('Sales', conn, if_exists='replace', index=False)
    dim_customer.to_sql('Customers', conn, if_exists='replace', index=False)
    conn.close()
    print("Demo veritabanı oluşturuldu: sales.db")

if __name__ == '__main__':
    create_demo_db()