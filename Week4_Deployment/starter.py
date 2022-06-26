import pickle
import pandas as pd
import os, pathlib, sys
from pathlib import Path
import numpy as np
import pickle


def load_dic_vectorizer(bin_file):
    with open(bin_file, 'rb') as f_in:
        dv, lr = pickle.load(f_in)
    return dv, lr


def read_data(filename):
    df = pd.read_parquet(filename, engine="pyarrow")
    
    df['duration'] = df.dropOff_datetime - df.pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()
    categorical = ['PUlocationID', 'DOlocationID']
    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df

def preprocessing(year_input, month_input):
    df = read_data(f'https://nyc-tlc.s3.amazonaws.com/trip+data/fhv_tripdata_{year_input}-{month_input}.parquet')
    categorical = ['PUlocationID', 'DOlocationID']
    dv, lr = load_dic_vectorizer('model.bin')
    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    return lr, X_val, df

def main(year_input, month_input):
    lr, X_val, df = preprocessing(year_input, month_input)
    y_pred = lr.predict(X_val)
    y_pred_avg = np.mean(y_pred)

    year = pd.DatetimeIndex(df['pickup_datetime']).year
    month = pd.DatetimeIndex(df['pickup_datetime']).month

    year = year.astype('string')
    month = month.astype('string')

    df['ride_id'] = f'{year_input}/{month_input}_' + df.index.astype('str')
    df['prediction'] = y_pred
    df_result = df[['ride_id','prediction']]

    avg_pred = np.mean(list(df_result['prediction']))
    avg_pred = round(avg_pred, 3)
    print(avg_pred)


if __name__ == "__main__":
    year_input = (sys.argv[1]) if len(sys.argv) > 1 else "2021"
    month_input = (sys.argv[2]) if len(sys.argv) > 2 else "01"
    main(year_input, month_input)
