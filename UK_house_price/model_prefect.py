import os, sys, datetime
import pandas as pd
from prophet import Prophet
import statsmodels.api as sm

from pathlib import Path

import mlflow
from prefect import task, flow, get_run_logger
from prefect.task_runners import SequentialTaskRunner


@task(name="get-path-task")
def get_paths() -> str:
    '''Returning path to dataset in string format'''
    PATH_CURRENT = Path.cwd()
    DATA_PATH = os.path.join(PATH_CURRENT, "data", "Average_price-2022-06_from1995.csv")
    return DATA_PATH


@task(name="read-csv-task")
def read_data(path: str) -> pd.DataFrame:
    '''Reading data from given path'''
    logger = get_run_logger()
    logger.info("INFO reading csv files.")
    df = pd.read_csv(path)
    df2 = df.drop("Unnamed: 0", axis=1)
    df2["Date"] = pd.to_datetime(df2.Date)
    col1 = ["Average_Price", "Average_Price_SA"]
    col2 = ["Monthly_Change", "Annual_Change"]
    df2[col1] = df2[col1].astype("float32")
    df2[col2] = df2[col2].astype("float16")
    return df2


@task(name="decompose-time-series")
def decompose(df: pd.DataFrame, region_input: str):
    '''Breakdown of seasonal decomposition of time-series'''
    region_place = df[df["Region_Name"] == region_input]
    region_mean_price = region_place.groupby("Date")["Average_Price"].max()
    decomposition = sm.tsa.seasonal_decompose(region_mean_price, model="additive")
    fig = decomposition.plot()

    return region_mean_price


@task(name="forecast-prophet")
def forecast_prophet(df: pd.DataFrame):
    '''Fitting Prophet model to dataframe and generating forecasting graphs'''
    # Prepare the data in pandas dataframe
    model_df = pd.DataFrame(df).reset_index()
    model_df = model_df.rename(columns={"Date": "ds", "Average_Price": "y"})

    # Initialise the model and make predictions
    m = Prophet()
    m.fit(model_df)

    future = m.make_future_dataframe(periods=24, freq="M")

    forecast = m.predict(future)

    # Visualise the prediction
    fig1 = m.plot(forecast)


@task(name="divide-data")
def data_split(df: pd.DataFrame, region_input: str, split_date: str):
    '''Splitting data based on input region and date'''
    df = df[df["Region_Name"] == region_input]
    # split_date = "2018-01-01"
    df_train = df.loc[df["Date"] <= split_date].copy()
    df_test = df.loc[df["Date"] > split_date].copy()
    df_train = df_train[["Date", "Average_Price"]].rename(
        columns={"Date": "ds", "Average_Price": "y"}
    )
    df_test = df_test[["Date", "Average_Price"]].rename(
        columns={"Date": "ds", "Average_Price": "y"}
    )

    return df_train, df_test


@task(name="train-data")
def train_data(df_train: pd.DataFrame, region_input: str):
    '''Fitting Prophet model to training data'''
    logger = get_run_logger()

    model = Prophet()
    model.fit(df_train)

    logger.info(f"INFO Training Prophet on train set of {region_input}.")

    y_forecast = model.predict(df_train)

    y_pred_low, y_pred_up = max(y_forecast["yhat_lower"]), max(y_forecast["yhat_upper"])

    y_pred_additive, y_pred_low_additive, y_pred_up_additive = (
        max(y_forecast["additive_terms"]),
        max(y_forecast["additive_terms_lower"]),
        max(y_forecast["additive_terms_upper"]),
    )

    logger.info(f"Lower bound of prediction is: {y_pred_low}")
    logger.info(f"Upper bound of prediction is: {y_pred_up}")

    logger.info(f"Additive term of prediction is: {y_pred_additive}")
    logger.info(f"Lower additive term of prediction is: {y_pred_low_additive}")
    logger.info(f"Upper additive term of prediction is: {y_pred_up_additive}")
    logger.info(f"INFO Training Prophet finishes.")
    return model


@task(name="Forecast-test-data")
def evaluation(df_test: pd.DataFrame, model):
    '''Generalizing testing data with trained Prophet model'''
    logger = get_run_logger()
    logger.info("INFO running model.")

    y_predict = model.predict(df_test)
    y_pred_low, y_pred_up = max(y_predict["yhat_lower"]), max(y_predict["yhat_upper"])

    y_pred_additive, y_pred_low_additive, y_pred_up_additive = (
        max(y_predict["additive_terms"]),
       max(y_predict["additive_terms_lower"]),
        max(y_predict["additive_terms_upper"]),
    )

    logger.info(f"Lower bound of prediction is: {y_pred_low}")
    logger.info(f"Upper bound of prediction is: {y_pred_up}")

    logger.info(f"Additive term of prediction is: {y_pred_additive}")
    logger.info(f"Lower additive term of prediction is: {y_pred_low_additive}")
    logger.info(f"Upper additive term of prediction is: {y_pred_up_additive}")
    logger.info(f"INFO Forecasting finishes.")
    return y_predict


@flow(name="UK-house-price-flow")
def main():
    mlflow.set_tracking_uri("sqlite:///mlflow_uk_house.db")
    ### Create new experiment with S3 to keep learning information inside S3 bucket
    # s3_bucket = "s3://mlopszoomcamp-bucket/UK_house_price/"
    # mlflow.create_experiment("UK_house_price_forecasting", s3_bucket)
    mlflow.set_experiment("UK_house_price_forecasting")
    data_path = get_paths()
    df = read_data(data_path)
    region = sys.argv[1] # "Oxford"
    date = sys.argv[2] # "2019-01-01"

    with mlflow.start_run(run_name="Prophet_forecasting"):
        
        mlflow.set_tag("Region", region)
        mlflow.set_tag("Split Date", date)
        df_train, df_test = data_split(df, region, date)
        model = train_data(df_train, region)
        y_predict = evaluation(df_test, model)
        mlflow.log_metric("yhat_lower", max(y_predict["yhat_lower"]))
        mlflow.log_metric("yhat_upper", max(y_predict["yhat_upper"]))

        mlflow.log_metric("additive_terms", max(y_predict["additive_terms"]))
        mlflow.log_metric("additive_terms_lower", max(y_predict["additive_terms_lower"]))
        mlflow.log_metric("additive_terms_upper", max(y_predict["additive_terms_upper"]))

        
        mlflow.prophet.log_model(model, artifact_path="models_prophet")
        print(f"Default artifacts URI: '{mlflow.get_artifact_uri()}'")


if __name__ == "__main__":
    main()
