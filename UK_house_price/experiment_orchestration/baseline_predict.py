# pylint: disable=invalid-name,missing-module-docstring

import os
import pickle
import sys
from pathlib import Path

import pandas as pd


def load_model(region: str):
    """Loading model from previously trained Prophet model"""
    MODEL_FILE = os.getenv("MODEL_FILE", f"models/model_prophet_{region}.bin")
    with open(MODEL_FILE, "rb") as f_in:
        model = pickle.load(f_in)
    return model


def read_data(input_file):
    """Reading data from given path"""
    col1 = ["Average_Price", "Average_Price_SA"]
    col2 = ["Monthly_Change", "Annual_Change"]
    print("Reading data ...")
    df = pd.read_csv(input_file)
    df2 = df.drop("Unnamed: 0", axis=1)
    df2["Date"] = pd.to_datetime(df2.Date)
    df2[col1] = df2[col1].astype("float32")
    df2[col2] = df2[col2].astype("float16")
    return df2


def take_data(input_file, region_input: str, date: str):
    """Preparing test data after reading data"""
    df = read_data(input_file)
    print(f"Preparing data on region {region_input}...")
    df = df[df["Region_Name"] == region_input]
    split_date = date
    df_test = df.loc[df["Date"] > split_date].copy()
    df_test = df_test[["Date", "Average_Price"]].rename(
        columns={"Date": "ds", "Average_Price": "y"}
    )
    return df_test


def evaluation(df_test: pd.DataFrame, region: str):
    """Generalizing testing data with trained Prophet model"""
    model = load_model(region)
    print("Predicting model ...")
    y_predict = model.predict(df_test)

    return y_predict


def merge_result(y_hat, df_test, output_file, run_id):
    """Merging prediction result with test data"""
    df_result = pd.merge_asof(y_hat, df_test, on="ds")
    df_result["diff"] = df_result["y"] - df_result["yhat"]
    df_result["model_version"] = run_id
    print("Saving results to parquet ...")
    df_result.to_parquet(output_file, index=False)


def main():
    """Main program that run prediction on splitted dataset"""
    region = sys.argv[1]  # "Oxford"
    date = sys.argv[2]  # "2019-01-01"

    NEW_PATH = os.path.join(Path.cwd().parents[0], "data")
    input_file = os.path.join(NEW_PATH, "Average_price-2022-06_from1995.csv")
    ### Folder `output` must exist before running this file

    df = take_data(input_file, region, date)
    yhat = evaluation(df, region)

    y_hat = yhat["yhat"]
    y_hat_upper = yhat["yhat_upper"]
    y_hat_lower = yhat["yhat_lower"]
    print(
        f"""Prediction: yhat = {y_hat};
                yhat_upper = {y_hat_upper}; yhat_lower = {y_hat_lower}"""
    )


if __name__ == "__main__":
    main()