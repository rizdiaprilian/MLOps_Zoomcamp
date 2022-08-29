import os
import pickle

import requests
from flask import Flask
from flask import request
from flask import jsonify
import pandas as pd
from prophet import Prophet
from pymongo import MongoClient


MODEL_FILE = os.getenv('MODEL_FILE', 'model_prophet_Oxford.bin')

EVIDENTLY_SERVICE_ADDRESS = os.getenv('EVIDENTLY_SERVICE', 'http://127.0.0.1:5000')
MONGODB_ADDRESS = os.getenv("MONGODB_ADDRESS", "mongodb://127.0.0.1:27017")

with open(MODEL_FILE, 'rb') as f_in:
    model = pickle.load(f_in)


app = Flask('price-forecasting')
mongo_client = MongoClient(MONGODB_ADDRESS)
db = mongo_client.get_database("prediction_service")
collection = db.get_collection("data_forecasting")


@app.route('/predict', methods=['POST'])
def predict():
    record = request.get_json()
    key_features = ['ds', 'y']
    dict2 = {x:[record[x]] for x in key_features}


    feature_df = pd.DataFrame.from_dict(dict2)
    y_pred = model.predict(feature_df)
    pred = y_pred.to_dict("records")

    result = {
        'y_hat': pred[0]['yhat'],
        'y_hat_lower' : pred[0]['yhat_lower'],
        'y_hat_upper' : pred[0]['yhat_upper'],
    }

    rec = record.copy()
    rec['pred'] = result['y_hat']
    rec['pred_low'] = result['y_hat_lower']
    rec['pred_high'] = result['y_hat_upper']

    print(rec)
    ## Change from features dict to records dict
    save_to_db(record, result['y_hat'], result['y_hat_lower'], result['y_hat_upper'])
    send_to_evidently_service(record, result['y_hat'], result['y_hat_lower'], result['y_hat_upper'])
    return jsonify(result)

## Saving to MongoDB
def save_to_db(record, prediction, pred_low, pred_high):
    rec = record.copy()
    rec['pred'] = prediction
    rec['pred_low'] = pred_low
    rec['pred_high'] = pred_high
    collection.insert_one(rec)

# ## Saving to Evidently for monitoring
def send_to_evidently_service(record, prediction, pred_low, pred_high):
    rec = record.copy()
    rec['pred'] = prediction
    rec['pred_low'] = pred_low
    rec['pred_high'] = pred_high
    requests.post(f"{EVIDENTLY_SERVICE_ADDRESS}/iterate/uk_house_price", json=[rec])


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)