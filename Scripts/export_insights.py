import os
import pandas as pd # type: ignore
import mysql.connector # type: ignore

# Database connection settings
db_config = {
    'host': 'localhost',
    'user': 'etl_user',       
    'password': 'StrongPassword123#',  
    'database': 'retail_db'
}

# Folder to store CSVs
output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')
os.makedirs(output_dir, exist_ok=True)

# Function to run query and export to CSV
def export_query_to_csv(query, filename):
    conn = mysql.connector.connect(**db_config)
    df = pd.read_sql(query, conn)
    conn.close()
    path = os.path.join(output_dir, filename)
    df.to_csv(path, index=False)
    print(f"✅ Saved: {filename}")

# Queries
queries = {
    "top_products.csv": """
        SELECT product_name, SUM(quantity_sold) AS total_quantity
        FROM sales_data
        GROUP BY product_name
        ORDER BY total_quantity DESC
        LIMIT 10;
    """,
    "store_revenue.csv": """
        SELECT store_id, SUM(quantity_sold * unit_price) AS total_revenue
        FROM sales_data
        GROUP BY store_id
        ORDER BY total_revenue DESC;
    """,
    "monthly_revenue.csv": """
        SELECT DATE_FORMAT(date, '%Y-%m') AS month,
               SUM(quantity_sold * unit_price) AS monthly_revenue
        FROM sales_data
        GROUP BY month
        ORDER BY month;
    """,
    "category_revenue.csv": """
        SELECT category, SUM(quantity_sold * unit_price) AS total_revenue
        FROM sales_data
        GROUP BY category
        ORDER BY total_revenue DESC;
    """
}


for filename, query in queries.items():
    export_query_to_csv(query, filename)

print("\n All insights exported successfully to the 'output' folder!")
