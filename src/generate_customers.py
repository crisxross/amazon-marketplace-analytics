import pandas as pd
import numpy as np
from datetime import date  # <--- Added this to handle dates safely
from faker import Faker
from db_connection import engine  # Imports the database engine we tested!

# Initialize Faker with an Indian locale for realistic names/cities
fake = Faker("en_IN")

# Define how many customers we want to create
NUM_CUSTOMERS = 100_000

# Set a random seed so the random data is reproducible
np.random.seed(42)

# Creates an empty list bucket where we will store each newly generated customer dictionary
customers = []

print("Generating customer data... Please wait a moment.")

# The Loop (Generating 100,000 Customers)
for i in range(1, NUM_CUSTOMERS + 1):
    # Randomly assign gender based on set probabilities
    gender = np.random.choice(
        ["Male", "Female", "Other"],
        p=[0.48, 0.48, 0.04]
    )

    # Building the Customer Record Dictionary
    customer = {
        "customer_id": f"CUS{i:06d}",
        "customer_name": fake.name(),
        "gender": gender,
        "date_of_birth": fake.date_of_birth(minimum_age=18, maximum_age=70),
        "city": fake.city(),
        "state": fake.state(),
        "country": "India",
        # Using Python's date(year, month, day) object so Faker never throws a parse error
        "signup_date": fake.date_between(
            start_date=date(2020, 1, 1),
            end_date=date(2026, 9, 15)
        ),
        "customer_segment": np.random.choice(
            ["Basic", "Regular", "Premium"],
            p=[0.45, 0.40, 0.15]
        )
    }

    # Adds this completed customer dictionary into our main list bucket
    customers.append(customer)

# Converting to a Pandas DataFrame & Previewing
df_customers = pd.DataFrame(customers)

print(f"Generated {len(df_customers)} customers successfully!")
print(df_customers.head())

# Loading the Data into MySQL
print("Loading Customers into MYSQL database...")
df_customers.to_sql(
    "dim_customer",
    con=engine,
    if_exists="append",
    index=False,
    chunksize=5000,
)

print("Customers loaded successfully into MySQL!")




