import os
import datetime
import mlflow
from mlflow.tracking import MlflowClient
from flask import Flask, request, jsonify
import datetime
import pickle
import pandas as pd
import boto3

# ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID', "AKIARBMT65NSJIDOVSB3")
# SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', "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")
# client = boto3.client(
#     's3',
#     aws_access_key_id=ACCESS_KEY,
#     aws_secret_access_key=SECRET_KEY
# )


RUN_ID = os.getenv('RUN_ID', "a83db8840d254e9095dfe0ed2bc92158")
S3_BUCKET = os.getenv('S3_BUCKET', "mlopszoomcamp-bucket")
REGION = os.getenv('REGION', "Oxford")

### from S3 without tracking server ###
logged_model = f's3://{S3_BUCKET}/UK_house_price/{RUN_ID}/artifacts/models_prophet'
model = mlflow.pyfunc.load_model(logged_model)



with open('model_prophet_Oxford.bin', 'rb') as f_in:
    model = pickle.load(f_in)


def prepare_features(df_test):
    features = {}
    features['ds'] = df_test['ds']
    features['y'] = df_test['y']

    feature_df = pd.DataFrame.from_dict(features)
    return feature_df


def predict(features):
    preds = model.predict(features)
    return preds.to_dict("records")


app = Flask('price-forecasting')

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    ride = request.get_json()

    features = prepare_features(ride)
    pred = predict(features)
    result = {
        'y_hat': pred[0]['yhat'],
        'y_hat_lower' : pred[0]['yhat_lower'],
        'y_hat_upper' : pred[0]['yhat_upper'],
        'date': datetime.datetime.strftime(pred[0]['ds'], "%Y-%m-%d"),
        'model_version': RUN_ID,
        'region': REGION
    }
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)