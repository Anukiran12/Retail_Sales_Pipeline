import mysql.connector # type: ignore

# MySQL connection configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'etl_user',       # or 'root' if you didn't create etl_user
    'password': 'StrongPassword123#',  # use your password
    'database': 'retail_db'
}

try:
    # Connect to MySQL
    conn = mysql.connector.connect(**DB_CONFIG)
    print("Connection Successful!")
    conn.close()
except mysql.connector.Error as err:
    print(f"Error: {err}")
