import database
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def cos_similarity(arr1,arr2):
  """Gets two arrays and returns their cosine similarity """
  D1 = [arr1]
  D2 = [arr2]
  similarity = cosine_similarity(D1,D2)[0][0]
  return similarity

def similar_stations_func(source, destination, source_check, destination_check):
  """Gets the source, destination, source_check and destination_check.
     Return two lists source_max_names and dest_max_names of length 5 """
  station_data = database.get_encoded_stations()
  model = SentenceTransformer("all-MiniLM-L6-v2")
  source_max_score = [0] * 5
  source_max_names = [""] * 5
  dest_max_score = [0] * 5
  dest_max_names = [""] * 5
  source_encoded = model.encode(source)
  dest_encoded = model.encode(destination)
  for i in range(len(station_data["Station_Name"])):
      if not source_check:
        source_score = cos_similarity(source_encoded, station_data["Station_Name_Encoded"][i])
        if source_score > source_max_score[0]:
            source_max_score.insert(0,source_score)
            source_max_names.insert(0,station_data["Station_Name"][i])
            source_max_score.pop()
            source_max_names.pop()
      if not destination_check:
        destination_score = cos_similarity(dest_encoded, station_data["Station_Name_Encoded"][i])
        if destination_score > dest_max_score[0]:
            dest_max_score.insert(0,destination_score)
            dest_max_names.insert(0,station_data["Station_Name"][i])
            dest_max_score.pop()
            dest_max_names.pop()
  return source_max_names, dest_max_names