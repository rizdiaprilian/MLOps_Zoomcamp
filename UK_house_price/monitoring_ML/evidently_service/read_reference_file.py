import os, logging
from typing import Dict
from typing import List
from typing import Optional

import flask
import pandas as pd
from pyarrow import parquet as pq
from flask import Flask
import yaml


def configure_service():
    # pylint: disable=global-statement
    config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.yaml")

    # try to find a config file, it should be generated via the data preparation script
    if not os.path.exists(config_file_path):
        logging.error("File %s does not exist", config_file_path)
        exit("Cannot find a config file for the metrics service. Try to check README.md for setup instructions.")

    with open(config_file_path, "rb") as config_file:
        config = yaml.safe_load(config_file)

    # for dataset_name, dataset_options in config["datasets"].items():
    #     reference_file = dataset_options['reference_file']
    #     logging.info(f"Load reference data for dataset {dataset_name} from {reference_file}")
    #     reference_data = pq.read_table(reference_file).to_pandas()
    #     ## Put preprocessing code below ##
    #     reference_data['duration'] = reference_data.lpep_dropoff_datetime - reference_data.lpep_pickup_datetime
    #     reference_data.duration = reference_data.duration.apply(lambda td: td.total_seconds() / 60)
    #     reference_data = reference_data[(reference_data.duration >= 1) & (reference_data.duration <= 60)]
    col1 = ["Average_Price", "Average_Price_SA"]
    col2 = ["Monthly_Change", "Annual_Change"]
    for dataset_name, dataset_options in config["datasets"].items():
        reference_file = dataset_options['reference_file']
        logging.info(f"Load reference data for dataset {dataset_name} from {reference_file}")
        reference_data = pd.read_csv(reference_file)
        df2 = reference_data.drop("Unnamed: 0", axis=1)
        df2["Date"] = pd.to_datetime(df2.Date)
        df2[col1] = df2[col1].astype("float32")
        df2[col2] = df2[col2].astype("float16")

    print(df2.head())

if __name__ == '__main__':
    configure_service()