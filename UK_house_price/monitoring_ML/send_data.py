import json
import uuid
from datetime import datetime
from time import sleep
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import requests

tabel = pd.read_csv("Average_price-2022-06_from1995.csv")
tabel = tabel[tabel["Region_Name"] == "Oxford"]
data2 = pa.Table.from_pandas(tabel).to_pylist()

class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)



with open("target.csv", 'w') as f_target:
    for row in data2:
        row['id'] = str(uuid.uuid4())
        del row['Unnamed: 0']
        target = row['Average_Price']
        row['ds'] = row['Date']
        row['y'] = row['Average_Price']
        f_target.write(f"{row['id']},{target}\n")
        
        ## Sending request to flask app 'price-forecasting' located in prediction_service directory
        resp = requests.post("http://127.0.0.1:9696/predict",
                             headers={"Content-Type": "application/json"},
                             data=json.dumps(row, cls=DateTimeEncoder)).json()

        print(f"prediction: {resp['y_hat']} with lower limit {resp['y_hat_lower']} and upper limit {resp['y_hat_upper']}")
        sleep(1)