import mysql.connector
from dotenv import load_dotenv
load_dotenv()
import os
import streamlit as st
import pymongo
import pandas as pd

password = os.getenv("db_pass")
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password = password,
    database = 'chatbot'
)
mycursor = mydb.cursor()

db_user = os.getenv("db_mongo_user")
db_pass = os.getenv("db_mongo_pass")
connection_string = f"mongodb+srv://{db_user}:{db_pass}@cluster0.irtbklj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = pymongo.MongoClient(connection_string)
db = client.get_database("train_chatbot")
station_col = db.get_collection("station_encoded")

def fetch_details(source, destination):
    """Gets the source and destination
        Returns the train details that has the given source and destination"""
    query = f"""select Train_No, Train_Name, Station_Name,Arrival_time, Departure_Time from train_data where 
                train_name in
                (select distinct(table1.train_name) from 
                (select * from train_data
                where Station_Name="{source}") as table1 inner join
                (select * from train_data
                where Station_Name = "{destination}") as table2
                on table1.train_name = table2.train_name
                where table1.seq < table2.seq);"""
    mycursor.execute(query)
    return mycursor.fetchall()

def get_station_names():
    """Gets all the station names from the database"""
    query = """select distinct Station_Name from train_data"""
    mycursor.execute(query)
    return mycursor.fetchall()

def check_station(station_name):
    """Gets the station name and checks if the station exists in database"""
    query = f"""select * from train_data where Station_Name = "{station_name}" """
    mycursor.execute(query)
    if mycursor.fetchall():
        return True
    else:
        return False
    
def get_encoded_stations():
    station_data = station_col.find({},{"_id":0})
    station_encoded_dict = {"Station_Name":[],"Station_Name_Encoded":[]} 
    for i in station_data:
        station_encoded_dict["Station_Name"].append(i["Station_Name"])
        station_encoded_dict["Station_Name_Encoded"].append(i["Station_Name_encoded"])
    station_encoded_df = pd.DataFrame(station_encoded_dict)
    return station_encoded_df