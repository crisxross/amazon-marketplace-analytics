import numpy as np
import pandas as pd
from datetime import timedelta
from faker import Faker
from db_connection import engine

fake = Faker()

print("Fetching orders from database for payments mapping...")
df_orders = pd.read_sql("SELECT order_key, order_date FROM fact_orders", con=engine)

total_records = len(df_orders)
batch_size = 50_000
num_batches = int(np.ceil(total_records / batch_size))

print(f"Starting generation of payment records for {total_records:,} orders across {num_batches} batches...")

for batch in range(num_batches):
    start_idx = batch * batch_size
    end_idx = min((batch + 1) * batch_size, total_records)
    df_chunk = df_orders.iloc[start_idx:end_idx]

    batch_data = []

    for i, (_, row) in enumerate(df_chunk.iterrows()):
        current_global_idx = start_idx + i + 1
        order_key = int(row["order_key"])
        order_date = pd.to_datetime(row["order_date"])

        # Payment usually occurs on the exact same day as the order
        payment_date = order_date
        payment_date_key = int(payment_date.strftime('%Y%m%d'))

        # Sequential, 100% unique Payment ID
        payment_id = f"PAY{current_global_idx:08d}"

        payment_method = np.random.choice(
            ["Credit Card", "Debit Card", "PayPal", "Gift Card", "Net Banking"],
            p=[0.45, 0.25, 0.15, 0.10, 0.05]
        )

        payment_status = np.random.choice(
            ["Completed", "Pending", "Failed", "Refunded"],
            p=[0.90, 0.04, 0.02, 0.04]
        )

        # Realistic transaction amount between $10.00 and $500.00
        payment_amount = round(float(np.random.uniform(10.0, 500.0)), 2)

        batch_data.append({
            "payment_id": payment_id,
            "order_key": order_key,
            "payment_date_key": payment_date_key,
            "payment_method": payment_method,
            "payment_amount": payment_amount,
            "payment_status": payment_status
        })

    df_batch = pd.DataFrame(batch_data)

    df_batch.to_sql(
        "fact_payments",
        con=engine,
        if_exists="append",
        index=False,
        chunksize=10_000
    )

    print(f"Batch {batch + 1}/{num_batches} completed: {end_idx:,} payment records loaded.")

print("\nSUCCESS: All payment records generated and loaded into fact_payments!")