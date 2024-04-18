import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()

password = os.getenv("db_pass")
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password = password, 
    database = 'chatbot'
)
mycursor = mydb.cursor()

query = """CREATE TABLE train_data (Train_No int, Train_Name varchar(255), SEQ int, Station_Code varchar(50), 
            Station_Name varchar(255), Arrival_time Time, Departure_Time Time, Distance int, 
            Source_Station varchar(255), Source_Station_Name varchar(255), Destination_Station varchar(255), 
            Destination_Station_Name varchar(255))"""
mycursor.execute(query)




