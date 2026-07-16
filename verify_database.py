import sqlite3

connection = sqlite3.connect("shipment_database.db")
cursor = connection.cursor()

cursor.execute("SELECT COUNT(*) FROM shipment")
print("Shipments:", cursor.fetchone()[0])

cursor.execute("SELECT COUNT(*) FROM product")
print("Products:", cursor.fetchone()[0])

connection.close()