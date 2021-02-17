import pandas as pd
import requests
import os

def get_datasource(datasource_id: str, token: str):
  environment = os.getenv("NODE_ENV", default="development")
  url = "http://localhost:4000/api/datasource?id={}".format(datasource_id) if environment == "development" \
     else "http://data.wundercell.com/api/datasource?id={}".format(datasource_id)
  r = requests.get(url, headers={token: "Bearer {}".format(token)})
  data = r.json()
  return data

def load_datasource(datasource_id: str) -> pd.DataFrame:
  # need a way to retrieve token 
  token = os.getenv("BEARER_TOKEN", default=None)
  payload = get_datasource(datasource_id, token)

  if payload["data"]["type"] == "REST":
      url = payload["data"]["url"]
      key = payload["data"]["key"]
      r = requests.get(url)
      data = r.json()

      return pd.DataFrame(data[key])
    
  if payload["data"]["type"] == "CSV":
      url = payload["data"]["url"]

      data = pd.read_csv(url) 

      return data

  if payload["data"]["type"] == "POSTGRES":
      url = payload["data"]["url"]
      query = payload["data"]["query"]
      # grab data from POSTGRES by using connection URL + SQL query
      # convert into dataframe
      data = pd.DataFrame([])

      return data
  
  return pd.DataFrame([])

