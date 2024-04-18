import mysql.connector
import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv()


password = os.getenv("db_pass")
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password = password
)
mycursor = mydb.cursor()

def create_database(database_name):
  query = f"CREATE DATABASE {database_name};"
  mycursor.execute(query)

create_database("chatbot")



