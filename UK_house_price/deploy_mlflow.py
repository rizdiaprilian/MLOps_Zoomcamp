import os
import pickle

import mlflow
from mlflow.tracking import MlflowClient
from flask import Flask, request, jsonify

RUN_ID = '76bef12346a54de882e50a508aab6a21'
MLFLOW_TRACKING_URI = 'http://127.0.0.1:5000'
# RUN_ID = os.getenv('RUN_ID')

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
client = MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)

# path = client.download_artifacts(run_id=RUN_ID, path='')
logged_model = f'runs:/{RUN_ID}/artifacts/models_prophet'
model = mlflow.pyfunc.load_model(logged_model)

def prepare_features(df_test):
    features = {}
    features['ds'] = df_test['ds']
    features['y'] = df_test['y']
    return features


def predict(features):
    preds = model.predict(features)
    return float(preds)


app = Flask('price-forecasting')

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    ride = request.get_json()

    features = prepare_features(ride)
    pred = predict(features)

    # result = {
    #     'duration': pred,
    #     'model_version': RUN_ID
    # }
    result = {
        'avg_price pred lower': pred['yhat_lower'],
        'avg_price pred upper': pred['yhat_upper'],
        'model_version': RUN_ID
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)