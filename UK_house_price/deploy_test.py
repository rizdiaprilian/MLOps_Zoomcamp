import requests
from datetime import datetime, date

today = date.today()
input_date = datetime.strptime("2019-01-19", "%Y-%m-%d")

df_test = {
    "ds": today.strftime("%Y-%d-%m"),
    "y": 250000
}

url = 'http://localhost:9696/predict'
response = requests.post(url, json=df_test)
print(response.json())

# print(df_test)