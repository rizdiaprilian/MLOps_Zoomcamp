### Project: UK House Price ###

# **UK House Price**

The practical implementation of MLOps on real-world case is showcased in this repository. UK house price is chosen as the center of project on the grounds many concerns of surge in property.

Link on description about [UK house price](https://www.gov.uk/government/publications/about-the-uk-house-price-index/about-the-uk-house-price-index)
[Report and download links](https://www.gov.uk/government/collections/uk-house-price-index-reports-2022)

So far, we have managed to register machine learning in MLFlow as well as writing script to be orchestrated and ready for production. This step will bring further the model to be able to respond from given request in environment: deployment.

Setup preparation for model deployment can be done either in batch (offline) that allow prediction on newly unseen data arrives in periodic schedule or in real-time streaming (online) that the model always runs to serve anytime. 

## **Initialization**

The practice follows the same order as what we have been learning in week term. The structures is as follow:
- Experimentation tracking with MLFlow
- Orchestration with Prefect Orion (Prefect 2.0.3 is used here)
- Deployment from AWS S3 and MLFlow with Flask application
- Monitoring with MongoDB, Evidently

## **Prophet Model**

Prophet is used to capture forecasting capability on increasing trend of UK house price. Provided below are training and prediction at baseline stage.

1) Baseline learning and [model_generation](https://github.com/rizdiaprilian/MLOps_Zoomcamp/blob/master/UK_house_price/baseline_learn.py). This file will generate a model trained on a specified region after splitted under a given date and it is stored inside directory `models`. For example, command `python baseline_learn.py Oxford "2019-01-01"` will generate `models_prophet_Oxford.bin` 
2) Then run the prediction on a selected region with [Baseline prediction](https://github.com/rizdiaprilian/MLOps_Zoomcamp/blob/master/UK_house_price/baseline_predict.py), e.g. `python baseline_predict.py Oxford "2019-01-01`.

## **Experimentation**

The baseline workflow descripted above is then furtherly enhanced MLFlow paired with AWS EC2 and S3 that give the experiment degrees of reproducibility and greater range of tracking capability. Database to store information comprises of inference metrics and parameters is SQLite; Orchestration agent to manage of running smaller unit functions is Prefect Orion.

### **Steps**
1) Open [Jupyter Notebook](https://github.com/rizdiaprilian/MLOps_Zoomcamp/blob/master/UK_house_price/mlflow_experiment.ipynb). Run the very first cell after setting tracking server. 
Launch MLFlow with command `mlflow server -h 0.0.0.0 -p 5000 --backend-store-uri sqlite:///mlflow_uk_house.db --default-artifact-root s3://mlopszoomcamp-bucket`

2) Run the following command as follows to open Prefect Orion:
```
prefect config set PREFECT_ORION_UI_API_URL="<Public IPv4 address>/api"
prefect config set PREFECT_API_URL="<Public IPv4 address>/api"
prefect orion start --host 0.0.0.0
```
3) to run the prediction [here](https://github.com/rizdiaprilian/MLOps_Zoomcamp/blob/master/UK_house_price/model_prefect.py). Command `python model_prefect.py Oxford "2019-01-01"` generates an artifact with several logs furtherly

## **Deployment**

### **MLFlow**


## **Monitoring Strategy**
- Batch Monitoring: Predictions are generated in batch within specified interval, e.g. every six hours, every day, or monthly basis. Common use cases utilizing batch prediction includes collaborative filtering, content-based recommendations. Running app from prediction service sends input merged with generated output in JSON format to the Mongo DB. Data stored within MongoDB is transformed into pandas format and is compared with reference data loaded directly from csv file. A program incorporating prediction pipeline and drift calculation takes both reference and current data to be compared on the grounds of selected features with the use of `ColumnMapping`. The task is separably manageable on each running function with Prefect Orion.

- Online Monitoring: This service generates predictions after receiving requests. A downside is that the service needs to fulfill the requirement of running model in prolonged period until the change notice is issued.  

Since Evidently has yet released the feature specified for assessing time-series prediction, data drift is the only measurement to be covered in this section. Both online and batch monitors are used in this project.

## **Prediction Service**
This service generates predictions on requested rows delivered by`send_data.py` and submit them to Evidently and MongoDB.  

![image](https://user-images.githubusercontent.com/42743243/187480203-91ea5fdd-1b90-4f3d-8e5c-f698453de426.png)




