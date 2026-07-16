import sqlite3
import csv

# Connect to the SQLite database
connection = sqlite3.connect("shipment_database.db")

# Create a cursor to execute SQL queries
cursor = connection.cursor()

# Open the first CSV file
with open("data/shipping_data_0.csv", "r") as file:

    reader = csv.DictReader(file)

    for row in reader:

        product_name = row["product"]

        # Check if the product already exists
        cursor.execute(
            "SELECT id FROM product WHERE name = ?",
            (product_name,)
        )

        result = cursor.fetchone()

        # If the product doesn't exist, insert it
        if result is None:

            cursor.execute(
                "INSERT INTO product (name) VALUES (?)",
                (product_name,)
            )

            product_id = cursor.lastrowid

        else:

            product_id = result[0]

        origin = row["origin_warehouse"]
        destination = row["destination_store"]
        quantity = int(row["product_quantity"])

        cursor.execute(
            """
            INSERT INTO shipment
            (product_id, quantity, origin, destination)
            VALUES (?, ?, ?, ?)
            """,
            (product_id, quantity, origin, destination)
        )

        print(product_name, product_id)



# Read shipping_data_2.csv and store shipment information

shipment_lookup = {}

with open("data/shipping_data_2.csv", "r") as file:

    reader = csv.DictReader(file)

    for row in reader:

        shipment_lookup[row["shipment_identifier"]] = {
            "origin": row["origin_warehouse"],
            "destination": row["destination_store"],
            "driver": row["driver_identifier"]
        }



shipment_products = {}

with open("data/shipping_data_1.csv", "r") as file:

    reader = csv.DictReader(file)

    for row in reader:

        shipment_id = row["shipment_identifier"]
        product_name = row["product"]

        if shipment_id not in shipment_products:
            shipment_products[shipment_id] = {}

        if product_name not in shipment_products[shipment_id]:
            shipment_products[shipment_id][product_name] = 0

        shipment_products[shipment_id][product_name] += 1



# Combine shipment_products with shipment_lookup

for shipment_id in shipment_products:

    shipment_info = shipment_lookup[shipment_id]

    origin = shipment_info["origin"]
    destination = shipment_info["destination"]

    for product_name, quantity in shipment_products[shipment_id].items():

        # Check whether the product already exists
        cursor.execute(
            "SELECT id FROM product WHERE name = ?",
            (product_name,)
        )

        result = cursor.fetchone()

        if result is None:

            cursor.execute(
                "INSERT INTO product (name) VALUES (?)",
                (product_name,)
            )

            product_id = cursor.lastrowid

        else:

            product_id = result[0]

        # Insert shipment record
        cursor.execute(
            """
            INSERT INTO shipment
            (product_id, quantity, origin, destination)
            VALUES (?, ?, ?, ?)
            """,
            (product_id, quantity, origin, destination)
        )

connection.commit()
connection.close()

