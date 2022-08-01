from pathlib import Path
import pandas as pd
import pickle

import batch
import model

from datetime import datetime
from pandas.testing import assert_frame_equal
from pandas import Timestamp

def dt(hour, minute, second=0):
    return datetime(2021, 1, 1, hour, minute, second)

def input_data():
    data = [
            (None, None, dt(1, 2), dt(1, 10)),
            (1, 1, dt(1, 2), dt(1, 10)),
            (1, 1, dt(1, 2, 0), dt(1, 2, 50)),
            (1, 1, dt(1, 2, 0), dt(2, 2, 1)),        
        ]

    columns = ['PUlocationID', 'DOlocationID', 'pickup_datetime', 'dropOff_datetime']
    df = pd.DataFrame(data, columns=columns)
    return df

def test_prepare_data():
    df = input_data()
    batch_service = batch.ModelService(None)

    prep = batch_service.prepare_features(df)
    prep_dict = prep.to_dict()

    expected_result = {
        'PUlocationID': {0: '-1', 1: '1'},
        'DOlocationID': {0: '-1', 1: '1'},
        'pickup_datetime': {0: Timestamp('2021-01-01 01:02:00'),
            1: Timestamp('2021-01-01 01:02:00')},
        'dropOff_datetime': {0: Timestamp('2021-01-01 01:10:00'),
            1: Timestamp('2021-01-01 01:10:00')},
        'duration': {0: 8.000000000000002, 1: 8.000000000000002}
        }


    df_expected = pd.DataFrame(expected_result)
    assert expected_result == prep_dict

    assert_frame_equal(prep, df_expected)

###################



def read_text(file):
    test_directory = Path(__file__).parent

    with open(test_directory / file, 'rt', encoding='utf-8') as f_in:
        return f_in.read().strip()


def test_base64_decode():
    base64_input = read_text('data.b64')

    actual_result = model.base64_decode(base64_input)
    expected_result = {
        "ride": {
            "PULocationID": 130,
            "DOLocationID": 205,
            "trip_distance": 3.66,
        },
        "ride_id": 256,
    }

    assert actual_result == expected_result


def test_prepare_features():
    model_service = model.ModelService(None)

    ride = {
        "PULocationID": 130,
        "DOLocationID": 205,
        "trip_distance": 3.66,
    }

    actual_features = model_service.prepare_features(ride)

    expected_fetures = {
        "PU_DO": "130_205",
        "trip_distance": 3.66,
    }

    assert actual_features == expected_fetures


