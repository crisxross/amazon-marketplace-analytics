import numpy as np
import pandas as pd
from datetime import timedelta
from faker import Faker
from db_connection import engine

fake = Faker()

print("Fetching orders from database for returns mapping...")
df_orders = pd.read_sql("SELECT order_key, order_date FROM fact_orders", con=engine)

# Simulating a realistic return rate of ~12% of total orders
num_returns = int(len(df_orders) * 0.12)
df_return_orders = df_orders.sample(n=num_returns, random_state=42).reset_index(drop=True)

batch_size = 50_000
num_batches = int(np.ceil(num_returns / batch_size))

print(f"Starting generation of {num_returns:,} return records across {num_batches} batches...")

for batch in range(num_batches):
    start_idx = batch * batch_size
    end_idx = min((batch + 1) * batch_size, num_returns)
    df_chunk = df_return_orders.iloc[start_idx:end_idx]

    batch_data = []

    for i, (_, row) in enumerate(df_chunk.iterrows()):
        current_global_idx = start_idx + i + 1
        order_key = int(row["order_key"])
        order_date = pd.to_datetime(row["order_date"])

        # Return occurs 5 to 25 days after the order date
        return_date = order_date + timedelta(days=int(np.random.randint(5, 26)))
        return_date_key = int(return_date.strftime('%Y%m%d'))

        # Sequential, 100% unique Return ID
        return_id = f"RET{current_global_idx:08d}"

        return_reason = np.random.choice(
            ["Defective Product", "Wrong Item Received", "Not as Described", "Changed Mind", "Arrived Too Late"],
            p=[0.30, 0.20, 0.20, 0.20, 0.10]
        )

        return_status = np.random.choice(
            ["Requested", "Approved", "Refunded", "Rejected"],
            p=[0.10, 0.15, 0.70, 0.05]
        )

        return_quantity = int(np.random.choice([1, 2, 3], p=[0.80, 0.15, 0.05]))
        refund_amount = round(float(np.random.uniform(15.0, 250.0)), 2)

        batch_data.append({
            "return_id": return_id,
            "order_key": order_key,
            "return_date_key": return_date_key,
            "return_reason": return_reason,
            "return_status": return_status,
            "return_quantity": return_quantity,
            "refund_amount": refund_amount
        })

    df_batch = pd.DataFrame(batch_data)

    df_batch.to_sql(
        "fact_returns",
        con=engine,
        if_exists="append",
        index=False,
        chunksize=10_000
    )

    print(f"Batch {batch + 1}/{num_batches} completed: {end_idx:,} return records loaded.")

print("\nSUCCESS: All return records generated and loaded into fact_returns!")
