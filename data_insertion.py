import pandas as pd
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

data = pd.read_csv("Train_details_22122017.csv")
null_mask = data.isnull().any(axis=1)

null_rows = data[null_mask]

cleaned_data = data.dropna()

def insert_into_table(cleaned_data):
    for i in range(len(cleaned_data)):
        first_row = dict(cleaned_data.iloc[i])
        columns = list(first_row.values())
        s_list = ["%s" for i in range(len(columns))]
        s_str = ", ".join(s_list)
        insert_query = f"""INSERT INTO train_data
                            VALUES ({s_str})"""
        mycursor.execute(insert_query, (columns))
        mydb.commit()

insert_into_table(cleaned_data)
    



