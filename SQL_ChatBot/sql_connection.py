# from mysql.connector import connect
import os
from dotenv import load_dotenv
import mysql.connector
import csv
import io

load_dotenv()
username = os.getenv("db_user")
password = os.getenv("db_password")
localhost = os.getenv("db_host")
db_name = os.getenv("db_name")


mydb = mysql.connector.connect(
  host=localhost,
  user=username,
  password=password,
  database=db_name
)

def sql_cursor():
  mycursor = mydb.cursor()
  return mycursor



def format_results_as_list(headers, rows):
    # Create the header row as a list
    header_row = [str(header) for header in headers]
    
    # Create the data rows as lists without padding for column width
    data_rows = [[str(value) for value in row] for row in rows]
    
    # Combine the header row and the data rows into a final list of lists
    table_as_list = [header_row] + data_rows
    
    return table_as_list



if __name__ == "__main__":
     mycursor = sql_cursor()
     mycursor.execute("SELECT * FROM `ground_water_level-2015-2022`")
     myresult = mycursor.fetchall()
     for x in myresult:
        print(x)
  


