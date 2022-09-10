## **Fitting Prophet Model**

Prophet is used to capture forecasting capability on increasing trend of UK house price. Provided below are training and prediction at baseline stage.

1) Baseline learning and [model_generation](https://github.com/rizdiaprilian/MLOps_Zoomcamp/blob/master/UK_house_price/baseline_learn.py). This file will generate a model trained on a specified region after splitted under a given date and it is stored inside directory `models`. For example, command `python baseline_learn.py Oxford "2019-01-01"` will generate `models_prophet_Oxford.bin`
2) Then run the prediction on a selected region with [Baseline prediction](https://github.com/rizdiaprilian/MLOps_Zoomcamp/blob/master/UK_house_price/baseline_predict.py), e.g. `python baseline_predict.py Oxford "2019-01-01`.

## **MLFlow Experimentation**

The baseline workflow descripted above is then furtherly enhanced MLFlow paired with AWS EC2 and S3 that give the experiment degrees of reproducibility and greater range of tracking capability. Database to store information comprises of inference metrics and parameters is SQLite; Orchestration agent to manage of running smaller unit functions is Prefect Orion.

### **Steps**
1) Open [Jupyter Notebook](https://github.com/rizdiaprilian/MLOps_Zoomcamp/blob/master/UK_house_price/mlflow_experiment.ipynb). Run the very first cell after setting tracking server.
Launch MLFlow with command `mlflow server -h 0.0.0.0 -p 5000 --backend-store-uri sqlite:///mlflow_uk_house.db --default-artifact-root s3://mlopszoomcamp-bucket`

![image](https://user-images.githubusercontent.com/42743243/187728007-28af1174-96ff-477c-ac7f-16f2cdb752ff.png)

2) Run the following command as follows to open Prefect Orion:
```
prefect config set PREFECT_ORION_UI_API_URL="<Public IPv4 address>/api"
prefect config set PREFECT_API_URL="<Public IPv4 address>/api"
prefect orion start --host 0.0.0.0
```

![image](https://user-images.githubusercontent.com/42743243/187728101-75ffe464-b34d-4c5a-8c24-15e7d93459e4.png)

3) Run the prediction [here](https://github.com/rizdiaprilian/MLOps_Zoomcamp/blob/master/UK_house_price/model_prefect.py). Command `python model_prefect.py Oxford "2019-01-01"` generates an artifact with several logs along with parameters and forecasting metrics and the logged model can be used for deployment.