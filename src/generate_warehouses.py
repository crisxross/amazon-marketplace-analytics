# ==========================================
# PART 1: IMPORTING NECESSARY LIBRARIES
# ==========================================
import pandas as pd                  # Handles data structuring into tabular DataFrames
import numpy as np                   # Handles array operations
from db_connection import engine     # Connects directly to our MySQL database bridge


# ==========================================
# PART 2: CONFIGURATION & SETUP
# ==========================================

# Define major Indian logistics hubs.
# Format:
# (City, State, Warehouse Name, Region, Warehouse Type)
hub_locations = [
    ("Mumbai", "Maharashtra", "BOM1 - Bhiwandi Fulfillment Center", "West", "Fulfillment Center"),
    ("Delhi", "Delhi", "DEL2 - Okhla Sorting Hub", "North", "Sorting Hub"),
    ("Bengaluru", "Karnataka", "BLR1 - Devanahalli Mega Hub", "South", "Mega Hub"),
    ("Chennai", "Tamil Nadu", "MAA1 - Sriperumbudur Fulfillment Center", "South", "Fulfillment Center"),
    ("Hyderabad", "Telangana", "HYD1 - Shamshabad Logistics Park", "South", "Logistics Park"),
    ("Kolkata", "West Bengal", "CCU1 - Dankuni Warehouse", "East", "Warehouse"),
    ("Pune", "Maharashtra", "PNQ1 - Chakan Distribution Center", "West", "Distribution Center"),
    ("Ahmedabad", "Gujarat", "AMD1 - Changodar Hub", "West", "Hub"),
    ("Jaipur", "Rajasthan", "JAI1 - Sitapura Industrial Hub", "North", "Industrial Hub"),
    ("Lucknow", "Uttar Pradesh", "LKO1 - Transport Nagar Center", "North", "Transport Center"),
    ("Kochi", "Kerala", "COK1 - Kalamassery Fulfillment Hub", "South", "Fulfillment Hub"),
    ("Guwahati", "Assam", "GAU1 - Changsari Logistics Center", "East", "Logistics Center")
]

# Empty list used to store warehouse dictionaries
warehouses = []

print("Generating strategic Indian warehouse fulfillment data...")


# ==========================================
# PART 3: THE GENERATION LOOP
# ==========================================

# enumerate() provides a sequential number for each warehouse.
# start=1 makes the first warehouse_key equal to 1.
for i, (city, state, wh_name, region, wh_type) in enumerate(hub_locations, start=1):

    warehouse = {
        # Primary key value
        "warehouse_key": i,

        # Warehouse ID formatted as WH001, WH002, ..., WH012
        "warehouse_id": f"WH{i:03d}",

        # Warehouse descriptive information
        "warehouse_name": wh_name,
        "city": city,
        "state": state,
        "country": "India",
        "region": region,
        "warehouse_type": wh_type
    }

    # Add the warehouse dictionary to the list
    warehouses.append(warehouse)


# ==========================================
# PART 4: CONVERTING TO A PANDAS DATAFRAME
# ==========================================

# Convert the list of dictionaries into a tabular DataFrame
df_warehouses = pd.DataFrame(warehouses)

print(f"Generated {len(df_warehouses)} warehouse hubs successfully!")

# Display the generated warehouse data
print(df_warehouses)


# ==========================================
# PART 5: LOADING DATA INTO MYSQL DATABASE
# ==========================================

print("Loading warehouses into MySQL database...")

# Insert the DataFrame records into the dim_warehouse table
df_warehouses.to_sql(
    "dim_warehouse",     # Target MySQL table
    con=engine,          # SQLAlchemy database connection
    if_exists="append",  # Add rows without deleting existing records
    index=False,         # Do not insert the Pandas index as a column
    chunksize=500        # Insert records in batches of up to 500 rows
)

print("Warehouses loaded successfully into MySQL!")




