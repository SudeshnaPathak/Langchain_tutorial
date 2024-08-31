import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
load_dotenv()
username = os.getenv("db_user")
password = os.getenv("db_password")
localhost = os.getenv("db_host")

# Load the Excel file into a DataFrame
df = pd.read_excel('Atal_Jal_Disclosed_Ground_Water_Level-2015-2022 (1).xlsx', sheet_name='Atal_Jal_Disclosed_Ground_Water')

# Create a SQLAlchemy engine for MySQL
engine = create_engine(f'mysql+mysqlconnector://{username}:{password}@{localhost}:3306/jalshaktimodels')

# Convert the DataFrame to a MySQL table
df.to_sql('ground_water_level-2015-2022', con=engine, if_exists='replace', index=False)