import os, datetime
import pandas as pd
import numpy as np
from prophet import Prophet
import statsmodels.api as sm

from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px


def get_paths() -> str:
    PATH_CURRENT = Path.cwd()
    NEW_PATH = os.path.join(PATH_CURRENT.parents[1], "data", "uk_house_price")
    DATA_PATH = os.path.join(NEW_PATH, "Average_price-2022-06_from1995.csv")
    return DATA_PATH


def read_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df2 = df.drop("Unnamed: 0", axis=1)
    df2["Date"] = pd.to_datetime(df2.Date)
    col1 = ["Average_Price", "Average_Price_SA"]
    col2 = ["Monthly_Change", "Annual_Change"]
    df2[col1] = df2[col1].astype("float32")
    df2[col2] = df2[col2].astype("float16")
    return df2


def decompose(df: pd.DataFrame, region_input: str):
    region_place = df[df["Region_Name"] == region_input]
    region_mean_price = region_place.groupby("Date")["Average_Price"].max()
    decomposition = sm.tsa.seasonal_decompose(region_mean_price, model="additive")
    fig = decomposition.plot()

    return region_mean_price


def forecast_prophet(df: pd.DataFrame):
    # Prepare the data in pandas dataframe
    model_df = pd.DataFrame(df).reset_index()
    model_df = model_df.rename(columns={"Date": "ds", "Average_Price": "y"})

    # Initialise the model and make predictions
    m = Prophet()
    m.fit(model_df)

    future = m.make_future_dataframe(periods=24, freq="M")

    forecast = m.predict(future)

    # Visualise the prediction
    m.plot(forecast)
    m.plot_components(forecast)


def main():
    # mlflow.set_tracking_uri("sqlite:///mlflow_prefect.db")
    # mlflow.set_experiment("prefect-experiment")
    data_path = get_paths()
    df = read_data(data_path)
    newcastle = decompose(df, "Newcastle upon Tyne")

    newcastle_forecast = forecast_prophet(newcastle)


if __name__ == "__main__":
    main()
