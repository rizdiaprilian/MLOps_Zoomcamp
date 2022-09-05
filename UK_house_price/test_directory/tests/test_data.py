from datetime import datetime
from pandas.testing import assert_frame_equal
from pandas import Timestamp
import pandas as pd



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