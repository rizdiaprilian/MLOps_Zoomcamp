from pathlib import Path
from datetime import datetime
from pandas.testing import assert_frame_equal
from pandas import Timestamp
import pandas as pd
import os, pickle
import numpy as np
# import model


def dt(year, month, day):
    return datetime(year, month, day)

def input_data():
    data = [
            (dt(2001, 6, 1), 'Newcastle upon Tyne', 'E060003', 189310, 2.3, 1.3, 146575),
            (dt(2003, 7, 15), 'Liverpool', 'F423103', 243400, 2.3, 2.3, 242358),
            (dt(2005, 9, 21), 'Kent', 'B80514', 142500, 2.3, 2.3, 134131), 
    ]

    columns = ['Date', 'Region_Name', 'Area_Code', 'Average_Price', 'Monthly_Change',
       'Annual_Change', 'Average_Price_SA']
    df = pd.DataFrame(data, columns=columns)
    df["Date"] = pd.to_datetime(df.Date)
    return df

def load_model():
    MODEL_FILE = os.getenv('MODEL_FILE', f'model_prophet_Oxford.bin')
    with open(MODEL_FILE, 'rb') as f_in:
        model = pickle.load(f_in)
    return model

def test_prepare_data():
    df = input_data()
    prep_dict = df.to_dict()

    expected_result = {
        'Date': {0: Timestamp('2001-06-01 00:00:00'), 1: Timestamp('2003-07-15 00:00:00'),
                    2: Timestamp('2005-09-21 00:00:00')},
        'Region_Name': {0: 'Newcastle upon Tyne', 1: 'Liverpool', 2: 'Kent'},
        'Area_Code': {0: 'E060003',
            1: 'F423103', 2: 'B80514'},
        'Average_Price': {0: 189310,
            1: 243400, 2: 142500},
        'Monthly_Change': {0: 2.3, 1: 2.3, 2: 2.3},
        'Annual_Change': {0: 1.3, 1: 2.3, 2: 2.3},
        'Average_Price_SA': {0: 146575, 1: 242358, 2: 134131}
        }

    df_expected = pd.DataFrame(expected_result)
    assert expected_result == prep_dict
    assert_frame_equal(df, df_expected)

def predict_features():
    df = input_data()
    data_prep = df[['Date','Average_Price']].rename(columns={'Date': 'ds', 'Average_Price': 'y'})
    expected_result = {
        'ds': {0: Timestamp('2001-06-01 00:00:00'), 1: Timestamp('2003-07-15 00:00:00'),
                    2: Timestamp('2005-09-21 00:00:00')},
        'y': {0: 189310, 1: 243400, 2: 142500},
        }

    df_expected = pd.DataFrame(expected_result)
    assert_frame_equal(data_prep, df_expected)
    model = load_model()
    y_predict = model.predict(data_prep)
    
    df_predict = y_predict[['ds','yhat','yhat_lower','yhat_upper']]
    merge_result = pd.merge(data_prep, df_predict, how="left", on="ds")
    merge_result['yhat'] = np.round(merge_result['yhat'], decimals = -4)
    merge_result['yhat_lower'] = np.round(merge_result['yhat_lower'], decimals = -4)
    merge_result['yhat_upper'] = np.round(merge_result['yhat_upper'], decimals = -4)

    result_dict = merge_result.to_dict()

    expected_prediction = {
        'ds': {0: Timestamp('2001-06-01 00:00:00'), 1: Timestamp('2003-07-15 00:00:00'),
                    2: Timestamp('2005-09-21 00:00:00')},
        'y': {0: 189310, 1: 243400, 2: 142500},
        'yhat': {0: 150000.0, 1: 160000.0, 2: 230000.0},
        'yhat_lower': {0: 140000.0, 1: 150000.0, 2: 210000.0},
        'yhat_upper': {0: 170000.0, 1: 180000.0, 2: 240000.0},
    }
    assert expected_prediction == result_dict

