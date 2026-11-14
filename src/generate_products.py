# ==========================================
# PART 1: IMPORTING NECESSARY LIBRARIES
# ==========================================
import pandas as pd                  # Library for handling tabular data (DataFrames)
import numpy as np                   # Library for math operations and random probability distribution
from datetime import date            # Python's built-in date tool to safely pass calendar dates
from faker import Faker              # Library to generate realistic fake data (dates, text, etc.)
from db_connection import engine     # Imports our pre-tested MySQL database connection bridge

# ==========================================
# PART 2: CONFIGURATION & SETUP
# ==========================================

# Initialize Faker with an Indian locale ('en_IN') so any default strings match Indian contexts
fake = Faker("en_IN")

# Define the exact number of products we want to generate for our data warehouse
NUM_PRODUCTS = 50_000

# Set a random seed (42) so the random data is reproducible (generates the exact same data every time it runs)
np.random.seed(42)

# ==========================================
# PART 3: DEFINING THE E-COMMERCE CATALOG
# ==========================================
# This dictionary structures our data logically. It pairs specific categories
# with matching subcategories and real, popular Indian marketplace brands.

catalog = {
    "Electronics": {
        "subcategories": ["Smartphones", "Laptops", "Wireless Earbuds", "Smart TVs"],
        "brands": ["Apple", "Samsung", "OnePlus", "Xiaomi", "Sony", "boAt", "Dell", "HP"]
    },
    "Home": {
        "subcategories": ["Cookware", "Water Bottles", "Mixer Grinders", "Bedsheets"],
        "brands": ["Prestige", "Milton", "Pigeon", "Bajaj", "Wakefit", "Solimo"]
    },
    "Fashion": {
        "subcategories": ["Jeans", "Sneakers", "T-Shirts", "Ethnic Kurtas"],
        "brands": ["Levi's", "Nike", "Puma", "Allen Solly", "FabIndia", "Biba"]
    },
    "Beauty": {
        "subcategories": ["Lipstick", "Facewash", "Shampoo", "Sunscreen"],
        "brands": ["Lakme", "Mamaearth", "Nykaa", "Maybelline", "L'Oreal", "Beardo"]
    },
    "Sports": {
        "subcategories": ["Cricket Bats", "Badminton Rackets", "Running Shoes", "Yoga Mats"],
        "brands": ["MRF", "SG", "Yonex", "Cosco", "Nivia", "Decathlon"]
    }
}

# Create an empty Python list bucket to temporarily store our generated product dictionaries
products = []

print("Generating realistic Indian marketplace product data... Please wait a moment.")

# ==========================================
# PART 4: THE GENERATION LOOP (50,000 ROWS)
# ==========================================
# Loop runs 50,000 times, where 'i' counts upward from 1 to 50,000
for i in range(1, NUM_PRODUCTS + 1):
    # Step A: Randomly pick a main category from our catalog dictionary keys
    category = np.random.choice(list(catalog.keys()))

    # Step B: Pick a subcategory and brand that strictly belong to that chosen category
    # (Prevents logical mismatches like an "Apple Cricket Bat")
    subcategory = np.random.choice(catalog[category]["subcategories"])
    brand = np.random.choice(catalog[category]["brands"])

    # Step C: Generate a realistic manufacturing cost price between 150 INR and 60,000 INR, rounded to 2 decimals
    cost_price = round(
        np.random.uniform(150, 60000),
        2
    )

    # Step D: Dynamically calculate a retail selling price by applying a random profit markup between 5% and 65% (1.05 to 1.65)
    selling_price = round(
        cost_price * np.random.uniform(1.05, 1.65),
        2
    )

    # Step E: Construct a structured dictionary representing a single product record
    product = {
        # Formats the ID neatly with leading zeros (e.g., PROD000001, PROD000002... up to PROD050000)
        "product_id": f"PROD{i:06d}",

        # Combines the brand and subcategory for a realistic Amazon-style product title
        "product_name": f"{brand} {subcategory} Model {i}",

        "category": category,
        "subcategory": subcategory,
        "brand": brand,
        "cost_price": cost_price,
        "selling_price": selling_price,

        # Generates a random calendar launch date between Jan 1, 2020 and Sep 15, 2026
        "launch_date": fake.date_between(
            start_date=date(2020, 1, 1),
            end_date=date(2026, 9, 15)
        ),

        # Generates a realistic e-commerce customer rating score between 3.0 and 5.0 stars
        "rating": round(
            np.random.uniform(3.0, 5.0),
            2
        )
    }

    # Step F: Append the completed product dictionary into our main list bucket
    products.append(product)

# ==========================================
# PART 5: CONVERTING TO PANDAS DATAFRAME
# ==========================================
# Transforms our raw list of 50,000 Python dictionaries into a structured, spreadsheet-like Pandas DataFrame
df_products = pd.DataFrame(products)

print(f"Generated {len(df_products)} realistic products successfully!")
print(df_products.head())  # Prints a preview of the first 5 rows to the console

# ==========================================
# PART 6: BATCH LOADING INTO MYSQL DATABASE
# ==========================================
print("Loading products into MySQL database...")

# Uses Pandas to_sql utility to write data directly into the database table
df_products.to_sql(
    "dim_product",       # Target table name in MySQL
    con=engine,          # Active database connection engine from db_connection.py
    if_exists="append",  # Appends rows into the table without dropping or overwriting its structure
    index=False,         # Disables saving Pandas internal row indices as an extra column
    chunksize=5000       # Pushes data in safe, manageable batches of 5,000 rows to prevent memory crashes
)

print("Products loaded successfully into MySQL!")