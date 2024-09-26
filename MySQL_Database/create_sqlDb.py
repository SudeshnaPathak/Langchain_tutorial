import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
load_dotenv()
username = os.getenv("db_user")
password = os.getenv("db_password")
localhost = os.getenv("db_host")

# Load the Excel file into a DataFrame
# df = pd.read_excel('ARS_Statistics_Data_of_Guntur ( Andhra Pradesh ).xlsx', sheet_name='ARS_Statistics_Data_of_Guntur (')

#Load the csv file
df = pd.read_csv('District_wise_Ground_Water_Resources_Data_of_Andhra_Pradesh_State_(In_ham)_of_2020 (1).csv')

# Create a SQLAlchemy engine for MySQL
engine = create_engine(f'mysql+mysqlconnector://{username}:{password}@{localhost}:3306/jalshaktimodels')

# Convert the DataFrame to a MySQL table
df.to_sql('ground_water_resources_data', con=engine, if_exists='replace', index=False)