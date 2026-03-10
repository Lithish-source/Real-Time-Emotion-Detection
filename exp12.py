import pandas as pd

# Example DataFrame
sales_data = pd.DataFrame({
    'product': ['Laptop', 'Phone', 'Tablet', 'Laptop', 'Phone', 'Headphones'],
    'quantity': [5, 10, 3, 7, 6, 8]
})

# Group by product and calculate total sales
total_sales = sales_data.groupby('product')['quantity'].sum()

# Sort and get top 5 products
top5_products = total_sales.sort_values(ascending=False).head(5)

print(top5_products)