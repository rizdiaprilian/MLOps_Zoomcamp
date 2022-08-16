import os
from datetime import datetime
import pandas as pd
import mlflow
from mlflow.tracking import MlflowClient
from flask import Flask, request, jsonify

RUN_ID = os.getenv('RUN_ID')
### with MLFLow tracking server ###
# RUN_ID = '836ad6fb72de4878a6cafb093bbeb2e3'
# MLFLOW_TRACKING_URI = 'http://ec2-35-177-90-140.eu-west-2.compute.amazonaws.com:5000'

# mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
# client = MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)

# logged_model = f'runs:/{RUN_ID}/models_prophet'

### from S3 without tracking server ###
logged_model = f's3://mlopszoomcamp-bucket/UK_house_price/{RUN_ID}/artifacts/models_prophet'
model = mlflow.pyfunc.load_model(logged_model)

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
        'date': datetime.strftime(pred[0]['ds'], "%Y-%m-%d"),
        'model_version': RUN_ID
    }
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)