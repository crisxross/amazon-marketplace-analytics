import numpy as np
import pandas as pd
from datetime import timedelta
from faker import Faker
from db_connection import engine

fake = Faker()

print("Fetching orders from database to map shipments to actual transactions...")
df_orders = pd.read_sql("SELECT order_key, order_date FROM fact_orders", con=engine)

total_records = len(df_orders)
batch_size = 50_000
num_batches = int(np.ceil(total_records / batch_size))

print(f"Starting generation of shipment records for {total_records:,} orders across {num_batches} batches...")

for batch in range(num_batches):
    start_idx = batch * batch_size
    end_idx = min((batch + 1) * batch_size, total_records)
    df_chunk = df_orders.iloc[start_idx:end_idx]

    batch_data = []

    for i, (_, row) in enumerate(df_chunk.iterrows()):
        current_global_idx = start_idx + i + 1
        order_key = int(row["order_key"])
        order_date = pd.to_datetime(row["order_date"])

        # 1. Shipment Date (1 to 2 days after order)
        shipment_date = order_date + timedelta(days=int(np.random.choice([1, 2], p=[0.7, 0.3])))
        shipment_date_key = int(shipment_date.strftime('%Y%m%d'))

        # 2. Expected Delivery Date (3 to 7 days after shipment)
        expected_days_add = int(np.random.choice([3, 4, 5, 7], p=[0.4, 0.3, 0.2, 0.1]))
        expected_delivery_date = shipment_date + timedelta(days=expected_days_add)
        expected_delivery_date_key = int(expected_delivery_date.strftime('%Y%m%d'))

        # 3. Delivery Status & Actual Delivery Date
        delivery_status = np.random.choice(
            ["Delivered", "In Transit", "Out for Delivery", "Delayed"],
            p=[0.85, 0.08, 0.04, 0.03]
        )

        if delivery_status == "Delivered":
            delay_offset = int(np.random.choice([-1, 0, 1, 2, 3], p=[0.2, 0.5, 0.15, 0.1, 0.05]))
            actual_delivery_date = expected_delivery_date + timedelta(days=delay_offset)
            actual_delivery_date_key = int(actual_delivery_date.strftime('%Y%m%d'))

            delivery_days = (actual_delivery_date - shipment_date).days
            delivery_delay_days = max(0, (actual_delivery_date - expected_delivery_date).days)
        else:
            actual_delivery_date_key = None
            delivery_days = None
            delivery_delay_days = None

        # 4. Sequential, 100% unique Shipment ID
        shipment_id = f"SHP{current_global_idx:08d}"
        warehouse_key = int(np.random.randint(1, 13))
        shipping_method = np.random.choice(
            ["Standard", "Express", "Prime Air", "Two-Day"],
            p=[0.50, 0.25, 0.15, 0.10]
        )

        batch_data.append({
            "shipment_id": shipment_id,
            "order_key": order_key,
            "warehouse_key": warehouse_key,
            "shipment_date_key": shipment_date_key,
            "expected_delivery_date_key": expected_delivery_date_key,
            "actual_delivery_date_key": actual_delivery_date_key,
            "shipping_method": shipping_method,
            "delivery_status": delivery_status,
            "delivery_days": delivery_days,
            "delivery_delay_days": delivery_delay_days
        })

    df_batch = pd.DataFrame(batch_data)

    df_batch.to_sql(
        "fact_shipments",
        con=engine,
        if_exists="append",
        index=False,
        chunksize=10_000
    )

    print(f"Batch {batch + 1}/{num_batches} completed: {end_idx:,} shipment records loaded.")

print("\nSUCCESS: All shipment records generated and loaded into fact_shipments!")