import requests
from datetime import datetime, date

today = date.today()
input_date = datetime.strptime("2019-01-25", "%Y-%m-%d")

## for pd.Dataframe
df_test = {
    "ds": [input_date.strftime("%Y-%m-%d")],
    "y": [270000]
}

url = 'http://localhost:9696/predict'
response = requests.post(url, json=df_test)
print(response.json())

# print(df_test)