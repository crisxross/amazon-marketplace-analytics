import numpy as np
import pandas as pd
from faker import Faker
from db_connection import engine  # Imports your SQLAlchemy connection engine

# Initialize Faker to generate realistic pseudo-data
fake = Faker()

print("Fetching product catalog from database to match actual prices...")
# Fetch existing products and prices from dim_product
# so our order items reference real catalog prices accurately.
df_products = pd.read_sql("SELECT product_key, selling_price FROM dim_product", con=engine)

# Configuration for bulk data generation
total_records = 500_000  # Total rows to generate
batch_size = 50_000  # Size of each batch to manage RAM and database load
num_batches = total_records // batch_size

print(f"Starting generation of {total_records:,} fact orders across {num_batches} batches...")

# Loop through batches to insert data incrementally
for batch in range(1, num_batches + 1):
    batch_data = []

    for _ in range(batch_size):
        # 1. Randomly sample a product from our fetched catalog DataFrame
        prod_row = df_products.sample(n=1).iloc[0]
        product_key = int(prod_row["product_key"])
        unit_price = float(prod_row["selling_price"])

        # 2. Assign foreign keys matching your dimension ranges
        customer_key = np.random.randint(1, 100_001)  # 100k customers (dim_customer)
        seller_key = np.random.randint(1, 1_001)  # 1,000 sellers (dim_seller)
        warehouse_key = np.random.randint(1, 13)  # 12 warehouses (dim_warehouse)

        # 3. Generate quantity with realistic probability distribution (mostly 1 or 2 items)
        quantity = np.random.choice([1, 2, 3, 4, 5], p=[0.60, 0.20, 0.10, 0.05, 0.05])

        # 4. Compute dependent financial fields
        total_amount = round(unit_price * quantity, 2)
        shipping_cost = round(np.random.uniform(20.0, 150.0), 2)  # Realistic shipping fees
#Note that total_amount currently excludes shipping. If your business definition includes shipping, you would calculate:
# total_amount = round((unit_price * quantity) + shipping_cost, 2)

        # 5. Generate descriptive/transaction attributes
        order_id = f"ORD{np.random.randint(10000000, 99999999)}"
        # Generates a random order date within the past 2 years up to today
        order_date = fake.date_between(start_date="-2y", end_date="today")

        # Realistic weighted probabilities for status and payment methods
        order_status = np.random.choice(
            ["Delivered", "Shipped", "Processing", "Cancelled", "Returned"],
            p=[0.75, 0.10, 0.05, 0.05, 0.05]
        )

        payment_method = np.random.choice(
            ["UPI", "Credit Card", "Debit Card", "Net Banking", "Cash on Delivery"],
            p=[0.45, 0.20, 0.15, 0.10, 0.10]
        )

        # Append row dictionary to the batch list
        batch_data.append({
            "order_id": order_id,
            "order_date": order_date,
            "customer_key": customer_key,
            "product_key": product_key,
            "seller_key": seller_key,
            "warehouse_key": warehouse_key,
            "quantity": quantity,
            "unit_price": unit_price,
            "total_amount": total_amount,
            "shipping_cost": shipping_cost,
            "order_status": order_status,
            "payment_method": payment_method
        })

    # Convert the completed batch list into a Pandas DataFrame
    df_batch = pd.DataFrame(batch_data)

    # Bulk insert the batch DataFrame into MySQL using SQLAlchemy chunks
    df_batch.to_sql(
        "fact_orders",
        con=engine,
        if_exists="append",
        index=False,
        chunksize=10_000
    )

    print(f"Batch {batch}/{num_batches} completed: {batch * batch_size:,} records successfully written to MySQL.")

print("\nSUCCESS: All 500,000 records generated and loaded into fact_orders!")