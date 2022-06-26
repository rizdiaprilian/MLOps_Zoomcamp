import requests
import starter_docker
import logging
import sys

year_input = (sys.argv[1]) if len(sys.argv) > 1 else "2021"
month_input = (sys.argv[2]) if len(sys.argv) > 2 else "01"

input_period = {
    "Year": year_input,
    "Month": month_input
}

url = 'http://localhost:9696/predict'
response = requests.post(url, json=input_period)
print(response.json())