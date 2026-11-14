# Import pandas for data manipulation, structuring rows, and handling tabular data
# Import SQLAlchemy to establish a connection bridge between Python and your MySQL database
# Import Faker to automatically generate realistic mock data (names, emails, dates, etc.)

import pandas as pd
import sqlalchemy
import faker

# Initialize Faker (this uses the import so PyCharm stops warning you)
fake = faker.Faker()

print("Python is working!")
print("Pandas version:", pd.__version__)
print("SQLAlchemy version:", sqlalchemy.__version__)
print("Faker is working!")