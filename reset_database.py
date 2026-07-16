import sqlite3

connection = sqlite3.connect("shipment_database.db")
cursor = connection.cursor()

cursor.execute("DELETE FROM shipment")
cursor.execute("DELETE FROM product")

connection.commit()
connection.close()

print("Database reset successfully!")