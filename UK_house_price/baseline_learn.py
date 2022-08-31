import os, sys
from pathlib import Path
import statsmodels.api as sm
import pandas as pd
from prophet import Prophet
import pickle


def get_paths() -> str:
    '''Returning path to dataset in string format'''
    PATH_CURRENT = Path.cwd()
    DATA_PATH = os.path.join(PATH_CURRENT, "data", "Average_price-2022-06_from1995.csv")
    return DATA_PATH


def read_data(path: str) -> pd.DataFrame:
    '''Reading data from given path'''
    df = pd.read_csv(path)
    df2 = df.drop("Unnamed: 0", axis=1)
    df2["Date"] = pd.to_datetime(df2.Date)
    col1 = ["Average_Price", "Average_Price_SA"]
    col2 = ["Monthly_Change", "Annual_Change"]
    df2[col1] = df2[col1].astype("float32")
    df2[col2] = df2[col2].astype("float16")
    return df2


def decompose(df: pd.DataFrame, region_input: str):
    '''Breakdown of seasonal decomposition of time-series'''
    region_place = df[df["Region_Name"] == region_input]
    region_mean_price = region_place.groupby("Date")["Average_Price"].max()
    decomposition = sm.tsa.seasonal_decompose(region_mean_price, model="additive")
    fig = decomposition.plot()

    return region_mean_price


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
    m.plot(forecast)
    m.plot_components(forecast)

def data_split(df: pd.DataFrame, region_input: str, split_date: str):
    '''Splitting data based on input region and date'''
    df = df[df["Region_Name"] == region_input]

    df_train = df.loc[df["Date"] <= split_date].copy()
    df_test = df.loc[df["Date"] > split_date].copy()
    df_train = df_train[["Date", "Average_Price"]].rename(
        columns={"Date": "ds", "Average_Price": "y"}
    )
    df_test = df_test[["Date", "Average_Price"]].rename(
        columns={"Date": "ds", "Average_Price": "y"}
    )

    return df_train, df_test

def train_data(df_train: pd.DataFrame):
    '''Fitting Prophet model to training data'''
    model = Prophet()
    model.fit(df_train)

    return model

def evaluation(df_test: pd.DataFrame, model):
    '''Generalizing testing data with trained Prophet model'''
    y_predict = model.predict(df_test)
    return y_predict

def main():
    data_path = get_paths()
    df = read_data(data_path)
    region = sys.argv[1] # "Oxford"
    date = sys.argv[2] # "2019-01-01"

    print(f"Splitting time-series of data slices of {region}...")    
    df_train, df_test = data_split(df, region, date)
    print("Training prophet model on train set...")
    model = train_data(df_train)
    print("Training finishes, proceed to evaluation...")
    y_predict = evaluation(df_test, model)
    y_hat=  y_predict["yhat"]
    y_hat_upper = y_predict["yhat_upper"]
    y_hat_lower = y_predict["yhat_lower"]
    print(f"""Prediction: yhat = {y_hat}; 
                yhat_upper = {y_hat_upper}; yhat_lower = {y_hat_lower}""")

    MODEL_FILE = os.getenv('MODEL_FILE', f'models/model_prophet_{region}.bin')
    with open(MODEL_FILE, 'wb') as f_in:
        pickle.dump(obj=model, file=f_in)


if __name__ == "__main__":
    main()
