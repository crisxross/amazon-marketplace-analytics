# ==========================================
# PART 1: IMPORTING NECESSARY LIBRARIES
# ==========================================
import pandas as pd                  # Library for structuring data into DataFrames
import numpy as np                   # Library for math and random distribution
from datetime import date            # Python date object manager
from faker import Faker              # Library for realistic names, cities, and states
from db_connection import engine     # Imports our active MySQL database engine

# ==========================================
# PART 2: CONFIGURATION & SETUP
# ==========================================

# Initialize Faker with an Indian locale ('en_IN') for realistic Indian cities and business entities
fake = Faker("en_IN")

# Define how many sellers we want to create (e.g., 1,000 active marketplace sellers)
NUM_SELLERS = 1_000

# Set a random seed (42) for reproducible data generation
np.random.seed(42)

# Pre-defined business suffixes and seller categories for the Indian market
business_suffixes = ["Enterprises", "Retail", "Traders", "E-Commerce", "Solutions", "Distributors", "Hub"]
seller_categories = ["Electronics Specialist", "Fashion & Apparel", "Home & Kitchen", "Beauty & Care", "General Merchandise"]

sellers = []

print("Generating realistic Indian marketplace seller data... Please wait a moment.")

# ==========================================
# PART 3: THE GENERATION LOOP (1,000 ROWS)
# ==========================================
for i in range(1, NUM_SELLERS + 1):
    
    # Generate a realistic business name using a last name or word combined with a business suffix
    company_name = f"{fake.last_name()} {np.random.choice(business_suffixes)}"
    
    seller = {
        # Formats seller ID cleanly with leading zeros (e.g., SEL000001 up to SEL001000)
        "seller_id": f"SEL{i:06d}",
        "seller_name": company_name,
        "seller_category": np.random.choice(seller_categories),
        "city": fake.city(),
        "state": fake.state(),
        "country": "India",
        
        # Generates a random vendor onboarding/join date between 2018 and 2026
        "join_date": fake.date_between(
            start_date=date(2018, 1, 1),
            end_date=date(2026, 9, 15)
        ),
        
        # Generates a realistic seller rating score between 3.2 and 5.0 stars
        "rating": round(
            np.random.uniform(3.2, 5.0),
            2
        )
    }

    # Append the completed seller dictionary into our main list bucket
    sellers.append(seller)

# ==========================================
# PART 4: CONVERTING TO PANDAS DATAFRAME
# ==========================================
df_sellers = pd.DataFrame(sellers)

print(f"Generated {len(df_sellers)} realistic sellers successfully!")
print(df_sellers.head())  # Prints a preview of the first 5 rows

# ==========================================
# PART 5: BATCH LOADING INTO MYSQL DATABASE
# ==========================================
print("Loading sellers into MySQL database...")

df_sellers.to_sql(
    "dim_seller",        # Target table name in MySQL
    con=engine,          # Active database connection bridge
    if_exists="append",  # Appends rows without overwriting table structure
    index=False,         # Disables saving Pandas internal row indices
    chunksize=500        # Pushes data in safe batches
)

print("Sellers loaded successfully into MySQL!")
