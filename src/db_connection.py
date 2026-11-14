import sqlalchemy

# Define your MySQL connection string
# Format: mysql+pymysql://username:password@host:port/database_name
# Note: Replace 'root' and 'your_password' with your actual MySQL credentials
db_user = "root"
db_password = "Bunty764020"  # Change this to your MySQL password
db_host = "localhost"
db_port = "3306"
db_name = "amazon_marketplace_analytics"

connection_string = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# Create the SQLAlchemy engine
engine = sqlalchemy.create_engine(connection_string)

try:
    # Test the connection by running a simple query
    with engine.connect() as connection:
        result = connection.execute(sqlalchemy.text("SELECT DATABASE();"))
        db_found = result.scalar()
        print(f"Successfully connected to MySQL! Active Database: {db_found}")
except Exception as e:
    print("Connection failed! Error:", e)