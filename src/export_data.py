import pandas as pd
from db_connection import engine

# Query your executive summary view using the SQLAlchemy engine
query = "SELECT * FROM vw_marketplace_executive_summary"
df = pd.read_sql(query, engine)

# Save as CSV inside the src folder
df.to_csv("src/marketplace_data.csv", index=False)
print("Exported successfully to src/marketplace_data.csv!")