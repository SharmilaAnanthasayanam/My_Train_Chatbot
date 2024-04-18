import database
from sentence_transformers import SentenceTransformer
import pandas as pd
import pprint
import data_insertion
import pymongo
import os
import pickle

# def convert_to_str(arr):
#     arr = list(map(str, arr))
#     return ", ".join(arr)

db_user = os.getenv("db_mongo_user")
db_pass = os.getenv("db_mongo_pass")
connection_string = f"mongodb+srv://{db_user}:{db_pass}@cluster0.irtbklj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = pymongo.MongoClient(connection_string)
db = client.get_database("train_chatbot")
station_col = db.get_collection("station_encoded")
print("Mongodb connected")

station_names = database.get_station_names()
station_df = pd.DataFrame(station_names, columns = ["Station_Name"])
model = SentenceTransformer("all-MiniLM-L6-v2")
station_df["Station_Name_encoded"] = station_df["Station_Name"].apply(model.encode)
print("station df created")
def converting_to_list(list_):
    return list_.tolist()
station_df["Station_Name_encoded"] = station_df["Station_Name_encoded"].apply(converting_to_list)
for index, row in station_df.iterrows():
    document = row.to_dict()
    station_col.insert_one(document)
print("station df inserted")


