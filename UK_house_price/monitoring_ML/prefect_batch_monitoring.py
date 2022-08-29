import json
import os
import pickle

import pandas as pd
from prefect import task, flow, get_run_logger
from prefect.task_runners import SequentialTaskRunner
from pymongo import MongoClient
import pyarrow.parquet as pq

from evidently import ColumnMapping

from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab

from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection, DataQualityProfileSection


@task(name="Target-Upload")
def upload_target(filename):
    """
    Upload rows of predicted values which are stored inside mongodb

    """
    logger = get_run_logger()
    logger.info("INFO Reading mongo database...")
    client = MongoClient("mongodb://localhost:27018/")
    logger.info("INFO Calling client prediction_service and retrieve collection data_forecasting...")
    collection = client.get_database("prediction_service").get_collection("data_forecasting")
    logger.info("INFO Updating collection on data_forecasting...")
    with open(filename) as f_target:
        for line in f_target.readlines():
            row = line.split(",")
            collection.update_one({"id": row[0]}, {"$set": {"target": float(row[1])}})
    logger.info("INFO Collection update from target.csv finishes...")


@task(name="Loading-Reference")
def load_reference_data(filename):
    """
    Load reference data and provide prediction result

    """
    logger = get_run_logger()
    logger.info("INFO Loading reference data...")
    MODEL_FILE = os.getenv('MODEL_FILE', './prediction_service/model_prophet_Manchester.bin')
    with open(MODEL_FILE, 'rb') as f_in:
        model = pickle.load(f_in)
    reference_data = pd.read_csv(filename)
    # Create features
    col1 = ["Average_Price", "Average_Price_SA"]
    col2 = ["Monthly_Change", "Annual_Change"]

    df2 = reference_data.drop("Unnamed: 0", axis=1)
    df2["Date"] = pd.to_datetime(df2.Date)
    df2[col1] = df2[col1].astype("float32")
    df2[col2] = df2[col2].astype("float16")
    df2 = df2[df2["Region_Name"] == "Oxford"]
    df2["ds"] = df2["Date"]
    df2["y"] = df2["Average_Price"]
    reference_data = df2.copy()

    # add target column
    logger.info("INFO Adding feature prediction output")
    features = ["ds", "y"]
    X_pred = reference_data[features]
    df_predict = model.predict(X_pred)
    df_predict_right = df_predict[['ds','yhat','yhat_lower','yhat_upper']]
    result = pd.merge(reference_data, df_predict_right, how="left", on="ds")
    reference_result = result.rename(columns={'yhat':'pred',
                     'yhat_lower':'pred_low',
                     'yhat_upper':'pred_high'})
    logger.info("INFO Reference data preparation complete...")
    return reference_result


@task(name="Data-Fetch-to-DataFrame")
def fetch_data():
    logger = get_run_logger()
    logger.info("INFO Load data_forecasting from mongodb...")
    client = MongoClient("mongodb://localhost:27018/")
    data = client.get_database("prediction_service").get_collection("data_forecasting").find()
    logger.info("INFO Transforming lists of dict to DataFrame...")
    list_data = list(data)
    df = pd.DataFrame(list_data[-330:])  ## for Oxford
    df['Date'] = pd.to_datetime(df['Date'])
    logger.info("INFO Dataframe of mongo dict complete...")
    return df


@task(name="Evidently-Dashboard-Profiling")
def run_evidently(ref_data: pd.DataFrame, data: pd.DataFrame):
    logger = get_run_logger()
    logger.info("INFO Run Evidently...")
    logger.info("INFO Initialize Drift Profiling and ColumnMapping...")
    profile = Profile(sections=[DataDriftProfileSection(), DataQualityProfileSection()])
    mapping = ColumnMapping(prediction="pred", numerical_features=['Average_Price','y','pred_low','pred_high'],
                            categorical_features=['Area_Code', 'Region_Name'],
                            datetime_features=["Date"])
    logger.info("INFO Calculating Drift Profile...")
    profile.calculate(ref_data, data, mapping)
    logger.info("INFO Dashboard Generating...")
    dashboard = Dashboard(tabs=[DataDriftTab()])
    dashboard.calculate(ref_data, data, mapping)
    return json.loads(profile.json()), dashboard


@task(name="Saving-Report-MongoDB")
def save_report(result):
    logger = get_run_logger()
    logger.info("INFO Saving Report to MongoDB...")
    client = MongoClient("mongodb://localhost:27018/")
    client.get_database("prediction_service").get_collection("report").insert_one(result[0])


@task(name="Saving-Report-HTML")
def save_html_report(result):
    logger = get_run_logger()
    logger.info("INFO Generating Report in HTML...")
    result[1].save("evidently_report_UK_house_price.html")


@flow(name="Batch-monitoring-flow")
def batch_analyze():
    upload_target("target.csv")
    ref_data = load_reference_data("./evidently_service/datasets/Average_price-2022-06_from1995.csv")
    data = fetch_data()
    result = run_evidently(ref_data, data)
    save_report(result)
    save_html_report(result)


if __name__ == "__main__":
    batch_analyze()
