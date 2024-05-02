import streamlit as st
import database
import pandas as pd
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
import similar_stations
import json
from streamlit_lottie import st_lottie
from streamlit_js_eval import streamlit_js_eval
from datetime import datetime, time


def load_lottiefile(filepath: str):
    """Gets the file path and returns the file in dict format"""
    with open(filepath, "r", encoding="utf8") as f:
        return json.load(f)

def UI_communication(value):
      """Gets the String and displays it with the animation"""
      st.markdown(f"<h4 style='text-align: center;'>{value}</h4>", unsafe_allow_html=True)
      lottie_streamlit = load_lottiefile("/content/Train_Animation.json")
      st.lottie(lottie_streamlit, speed=1.0, reverse = False, height=200)

def time_conversion(delta_time):
    """Converts seconds to hh:mm:ss format"""
    # Calculate the number of hours, minutes, and seconds
    hours = delta_time.seconds // 3600
    if hours < 10:
      hours = f"0{hours}"
    minutes = (delta_time.seconds % 3600) // 60
    if minutes < 10:
      minutes = f"0{minutes}"
    seconds = delta_time.seconds % 60
    if seconds < 10:
      seconds = f"0{seconds}"
    time_str = f"{hours}:{minutes}:{seconds}"
    # Convert string to time object
    time_obj = datetime.strptime(time_str, "%H:%M:%S").time()
    return time_obj

def audio_to_text(audio_path):
  """converts .wav file to text"""
  r = sr.Recognizer()
  with sr.AudioFile(audio_path) as source:
    audio_text = r.listen(source)
  try:
      # using google speech recognition
      text = r.recognize_google(audio_text)
      return(text)
  except:
      st.write('Sorry.. run again...')

def display_train_details(source, destination):
  """Gets source, destination and displays train details"""
  with placeholder.container():
    UI_communication("Loading...")
  train_details = database.fetch_details(source.upper(), destination.upper())
  train_df = pd.DataFrame(train_details, columns=["Train No","Train Name", "Station Name","Arrival Time", "Departure Time"])
  train_df["Arrival Time"] = train_df["Arrival Time"].apply(time_conversion)
  train_df["Departure Time"] = train_df["Departure Time"].apply(time_conversion)
  names = train_df["Train Name"].unique()
  placeholder.empty()
  with placeholder.container():
    if len(names):
      for train_name in names:
          source_data = train_df.loc[(train_df["Train Name"]==train_name) & (train_df["Station Name"]==source.upper())]
          destination_data = train_df.loc[(train_df["Train Name"]==train_name) & (train_df["Station Name"]==destination.upper() )]
          Train_no = source_data["Train No"].iloc[0]
          origin_station = source_data["Station Name"].iloc[0]
          src_arrival_time = source_data[["Departure Time"]].iloc[0,0]
          dest_station = destination_data["Station Name"].iloc[0]
          dest_arrival_time = destination_data[["Arrival Time"]].iloc[0,0]
          src_datetime = datetime.combine(datetime.today(), src_arrival_time)
          dest_datetime = datetime.combine(datetime.today(), dest_arrival_time)
          duration = dest_datetime - src_datetime
          hours = duration.seconds // 3600
          minutes = (duration.seconds % 3600) // 60
          seconds = duration.seconds % 60
          Duration = f"{hours} hrs {minutes} mins {seconds} secs"
          text = f"Train Name \t \t: {train_name} \n {origin_station} \t: {src_arrival_time} \n {dest_station} \t: {dest_arrival_time} \n Duration \t \t \t: {Duration} "
          st.text_area(f":green[**Train No: {Train_no}**]", text)
          with st.expander(f":blue[Train Full TimeTable]"):
              st.table(train_df.loc[train_df["Train Name"]==train_name])
    else:
      st.write("No trains found on your route")

col1, col2 = st.columns([0.85,0.15])
with col1:
  st.title(":orange[My Train Chatbot ]:metro:")
with col2: 
  if st.button("Home"):
    streamlit_js_eval(js_expressions="parent.window.location.reload()")

#Getting From and To locations as Text input 
placeholder = st.empty()
placeholder.empty()
with placeholder.container():
  source = st.text_input("From")
  destination = st.text_input("To")

#Getting From and to locations as audio input
audio_holder = st.empty()
text_holder = st.empty()
def get_audio():
  audio_bytes = audio_recorder(text="Click to check trains by voice",recording_color="#50C878")
  return audio_bytes

with audio_holder.container():
  audio_bytes = get_audio()
  st.write(":blue[Please provide voice input with 'From and To' pattern. \n Example: \
    I want to check trains that goes from chennai to banglore.]")

anime_holder = st.empty()
if audio_bytes:
  with anime_holder.container():
    UI_communication("Loading...")
  audio_path = "audio_file.wav"
  with open(audio_path, "wb") as f:
    f.write(audio_bytes)
  
  #Audio to Text Conversion
  text = audio_to_text(audio_path)
  anime_holder.empty()
  with text_holder.container():
    st.write(f":green[Your input: ] {text}")
  with anime_holder.container():
    UI_communication("Loading...")
  text.lower()
  if text.__contains__("from") and text.__contains__("to"):
    from_ind = text.index("from")
    text1 = text[from_ind+4:]
    to_index = text1.index("to")
    source = text1[:to_index]
    destination = text1[to_index+2:]
  else:
    anime_holder.empty()
    st.warning("Please provide voice input with from to pattern. \n Example: \
    I want to check trains that goes from chennai to banglore.")

#Checking if source and destination has been fetched
if source and destination:
    with anime_holder.container():
      UI_communication("Loading...")
    #Checking if source and destination locations are valid stations
    source_check = database.check_station(source)
    destination_check = database.check_station(destination)
    
    #If any of the location is invalid selection box is triggered and input is collected
    if not source_check or not destination_check:
      source_max_names, dest_max_names = similar_stations.similar_stations_func(source, 
        destination, source_check, destination_check)
      source_max_names.insert(0,"")
      dest_max_names.insert(0,"")
      src_option_holder = st.empty()
      dest_option_holder = st.empty()
      anime_holder.empty()
      if not source_check:
        with src_option_holder.container():
          source_station = st.selectbox("Choose your source station from the list below", source_max_names)
      else:
        source_station = source
      if not destination_check:
        with dest_option_holder.container():
          destination_station = st.selectbox("Choose your destination station from the list below", dest_max_names)
      else:
        destination_station = destination
      
      #Once we get the exact source and destintion stations updating the text boxes
      if source_station and destination_station:
          audio_holder.empty()
          src_option_holder.empty()
          dest_option_holder.empty()
          text_holder.empty()
          anime_holder.empty()
          with placeholder.container():
            source = st.text_input("From", value = source_station)
            destination = st.text_input("To", value = destination_station)
          check_holder=st.empty()
          with check_holder.container():
            check = st.button("Check")
          if check:
            placeholder.empty()
            audio_holder.empty()
            src_option_holder.empty()
            dest_option_holder.empty()
            text_holder.empty()
            with placeholder.container():
              UI_communication("Loading...")
            
            #Displaying the train details
            display_train_details(source, destination)
            check_holder.empty()
            # placeholder.empty()
    else:
        #if both source and destination stations are valid train details is displayed
        check_holder=st.empty()
        with check_holder.container():
          check = st.button("Check")
        if check:
          placeholder.empty()
          audio_holder.empty()
          with placeholder.container():
              UI_communication("Loading...")
          display_train_details(source, destination)
          check_holder.empty()
          # placeholder.empty()

      
        
      
              