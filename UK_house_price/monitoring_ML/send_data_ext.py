import os, json
import uuid
from datetime import datetime
from time import sleep
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import requests

import argparse
import time
from typing import Dict

tabel = pd.read_csv("Average_price-2022-06_from1995.csv")
tabel = tabel[tabel["Region_Name"] == "Oxford"]
data2 = pa.Table.from_pandas(tabel).to_pylist()

class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)


keys = ['ds', 'y']

with open("target.csv", 'w') as f_target:
    for row in data2:
        row['id'] = str(uuid.uuid4())
        del row['Unnamed: 0']
        target = row['Average_Price']
        row['ds'] = row['Date']
        row['y'] = row['Average_Price']
        f_target.write(f"{row['id']},{target}\n")
        dict2 = {x:[row[x]] for x in keys}
        ## Sending request to flask app 'price-forecasting' located in prediction_service directory
        resp = requests.post("http://127.0.0.1:9696/predict",
                             headers={"Content-Type": "application/json"},
                             data=json.dumps(dict2, cls=DateTimeEncoder)).json()

        print(f"prediction: {resp['y_hat']} with lower limit {resp['y_hat_lower']} and upper limit {resp['y_hat_upper']}")
        sleep(1)


def send_data_row(dataset_name: str, data: Dict) -> None:
    print(f"Send a data item for {dataset_name}")

    try:
        response = requests.post(
            f"http://127.0.0.1:9696/predict/{dataset_name}",
            data=json.dumps([data], cls=DateTimeEncoder),
            headers={"content-type": "application/json"},
        )

        if response.status_code == 200:
            print(f"Success.")

        else:
            print(
                f"Got an error code {response.status_code} for the data chunk. "
                f"Reason: {response.reason}, error text: {response.text}"
            )

    except requests.exceptions.ConnectionError as error:
        print(f"Cannot reach a metrics application, error: {error}, data: {data}")