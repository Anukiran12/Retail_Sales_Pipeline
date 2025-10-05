import pandas as pd # type: ignore
import mysql.connector # type: ignore
import os

# MySQL connection configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'etl_user',         # or 'root'
    'password': 'StrongPassword123#',
    'database': 'retail_db'
}

# List of CSV files (use absolute paths to avoid confusion)
csv_files = [
    r"C:\Users\Admin\OneDrive\Desktop\Retail Sales Pipeline\data\store_1.csv",
    r"C:\Users\Admin\OneDrive\Desktop\Retail Sales Pipeline\data\store_2.csv"
]

try:
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    total_rows = 0
    
    for file in csv_files:
        # Read CSV
        df = pd.read_csv(file)
        print(f"{os.path.basename(file)} has {len(df)} rows")
        print(df.head())  # prints first 5 rows to verify
        
        # Ensure columns match table
        df.columns = ['date', 'store_id', 'product_id', 'product_name', 'category', 'quantity_sold', 'unit_price']

        # Insert rows
        for i, row in df.iterrows():
            try:
                sql = """
                INSERT INTO sales_data (date, store_id, product_id, product_name, category, quantity_sold, unit_price)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, tuple(row))
            except Exception as e:
                print(f"Error inserting row {i} from {file}: {e}")
        
        conn.commit()
        total_rows += len(df)
        print(f"{len(df)} rows inserted from {os.path.basename(file)}")
    
    print(f"Total {total_rows} rows inserted successfully!")

except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    cursor.close()
    conn.close()
