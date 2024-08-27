import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
load_dotenv()
username = os.getenv("db_user")
password = os.getenv("db_password")
localhost = os.getenv("db_host")

# Load the Excel file into a DataFrame
df = pd.read_excel('NWMP_DATA_2021.xlsx', sheet_name='Table 1')

# Create a SQLAlchemy engine for MySQL
engine = create_engine(f'mysql+mysqlconnector://{username}:{password}@{localhost}:3306/jalshaktimodels')

# Convert the DataFrame to a MySQL table
df.to_sql('water_quality_data_ground_water', con=engine, if_exists='replace', index=False)