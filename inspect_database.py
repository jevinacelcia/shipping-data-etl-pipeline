import sqlite3

# Connect to the database
connection = sqlite3.connect("shipment_database.db")

cursor = connection.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

for table in tables:

    table_name = table[0]

    print(f"\nTable: {table_name}")

    cursor.execute(f"PRAGMA table_info({table_name});")

    columns = cursor.fetchall()

    for column in columns:
        print(column)

connection.close()