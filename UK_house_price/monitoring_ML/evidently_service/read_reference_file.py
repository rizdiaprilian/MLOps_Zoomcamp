import hashlib
import os

import dataclasses
import datetime
import logging
from typing import Dict
from typing import List
from typing import Optional

import pandas as pd

from pyarrow import parquet as pq
import yaml


config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.yaml")
if not os.path.exists(config_file_path):
    logging.error("File %s does not exist", config_file_path)
    exit("Cannot find a config file for the metrics service. Try to check README.md for setup instructions.")

with open(config_file_path, "rb") as config_file:
    config = yaml.safe_load(config_file)

for dataset_name, dataset_options in config["datasets"].items():
    reference_file = dataset_options['reference_file']
    logging.info(f"Load reference data for dataset {dataset_name} from {reference_file}")
    df = pd.read_csv(reference_file)
    col1 = ["Average_Price", "Average_Price_SA"]
    col2 = ["Monthly_Change", "Annual_Change"]

    df2 = df.drop("Unnamed: 0", axis=1)
    df2["Date"] = pd.to_datetime(df2.Date)
    df2[col1] = df2[col1].astype("float32")
    df2[col2] = df2[col2].astype("float16")
    df2 = df2[df2["Region_Name"] == "Oxford"]
    df2["ds"] = df2["Date"]
    df2["y"] = df2["Average_Price"]
    reference_data = df2.copy()
    print(reference_data.info())
    print("=================================================")
    print(dataset_name)
    print("=================================================")
    print(dataset_options)
    print("=================================================")
    print(dataset_options['monitors'])
    print("=================================================")
    print(dataset_options['column_mapping'])
        
        