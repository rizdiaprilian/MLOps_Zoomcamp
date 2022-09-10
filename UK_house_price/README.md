# **MLOps Final Project: UK House Price**

## **Problem Statement**

The practical implementation of MLOps to real-world case is showcased in this repository. UK house price is chosen as the center of project given the fact that the surge in property price in the UK raises concerns among public.

Link on description about [UK house price](https://www.gov.uk/government/publications/about-the-uk-house-price-index/about-the-uk-house-price-index)
The data source is available in [report and download links](https://www.gov.uk/government/collections/uk-house-price-index-reports-2022)

The aiming from working on this problem is to predict the volatility of surging prices within a period between January 2019 and June 2022. Metric used are:
  - y_hat: forecasting estimation
  - y_hat_lower: lower bound
  - y_hat_upper: upper bound

Prophet is used to meet its forecasting purpose. The information about Prophet is provided [here](https://github.com/facebook/prophet)


## **Initialization**

The practice follows the same order as what we have been learning in week term. The structures is as follow:
- Experimentation tracking with MLFlow
- Orchestration with Prefect Orion (Prefect 2.0.3 is used here)
- Deployment from AWS S3 and MLFlow with Flask application
- Monitoring with MongoDB, Evidently

### **Preparing Environment**

Environemt setting used here is `Pipfile` as the purpose is to gain better module utilization specified for this project. To launch the environment in `UK_house_price` directory, steps to be followed through are:
1) Run `pipenv install scikit-learn pandas prophet --version==3.9`. `Pipfile` and `Pipfile.lock` shall appear that collection of modules.
2) Enter the environment with command `pipenv shell`
3) To make it easier for writing command without clutter from relative directory, change with command `PS1="> "`

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

## **Deployment**
Experiment results stored in s3 bucket can be recalled to be used for deploying Prophet in Flask environment. See directory `deployment` to see the structures.
Steps to follow:
1) Set environment variables.
```
export RUN_ID="2a18236a06a346cd97a931f545d0be0f"
export REGION="Liverpool"
export S3_BUCKET="mlopszoomcamp-bucket"
```
3) Launch flask application with command `python deploy_mlflow.py`
4) See its response from flask with command `python deploy_test.py`

### **Deployment with Docker**
It is also possible to make a docker image for very same purpose. A little difference is that docker-compose will make use of environment variables defined in `.env` when starting the image.

1) Prepare required variables in `.env` then run command `docker build -t ${LOCAL_IMAGE_NAME} .` inside `deployment` directory. The image should be built there.
2) Execute `docker-compose run` to start the image.
3) Execute `python deploy_test.py`
4) If you wish to change, stop the image and replace values `RUN_ID` and `REGION` in `.env`. Then start the image again.

## **Monitoring Strategy**
- Batch Monitoring: Predictions are generated in batch within specified interval, e.g. every six hours, every day, or monthly basis. Common use cases utilizing batch prediction includes collaborative filtering, content-based recommendations. Running app from prediction service sends input merged with generated output in JSON format to the Mongo DB. Data stored within MongoDB is transformed into pandas format and is compared with reference data loaded directly from csv file. A program incorporating prediction pipeline and drift calculation takes both reference and current data to be compared on the grounds of selected features with the use of `ColumnMapping`. The task is separably manageable on each running function with Prefect Orion.

- Online Monitoring: This service generates predictions after receiving requests. A downside is that the service needs to fulfill the requirement of running model in prolonged period until the change notice is issued.

Since Evidently has yet released the feature specified for assessing time-series prediction, data drift is the only measurement to be covered in this section. Both online and batch monitors are used in this project.

Inside directory `monitoring_ML`, do:
1) Prepare four bash terminals, in which these terminals are used to: operate services with Docker compose, run Prefect Orion, 
2) Execute `docker-compose up` to start up service as follows: Prometheus, Grafana, MongoDB, and Evidently 
3) Run 'python send_data.py` to start sending data to MongoDB and Evidently monitoring service. An example of data drift monitoring in Grafana appears to be shown below
![image](https://user-images.githubusercontent.com/42743243/189478584-7df0ba1e-beef-4b59-afc0-70dad79f555c.png)
![image](https://user-images.githubusercontent.com/42743243/189479026-1fd76174-697c-4b57-99f0-94236c6f62fa.png)


4) Run 'python prefect_batch_monitoring.py' to produce a summary of data drift in HTML format. As this file, `evidently_report_UK_houe_price.html`, is too large in size, it is recommended to download first and open it in browser. 
![image](https://user-images.githubusercontent.com/42743243/189478594-326ecf97-0cef-484c-a3b7-b6992c5ec250.png)


## **Testing**

We wish to test how well the prediction works. AWS S3 localstack and Docker is used to serve this purpose. Again `.env` is provided to give environment variables for helping testing codes more loosely coupled.

1) Build docker inside `test_directory` as specified in `run_test.sh`. Then execute `docker-compose up` that will launch localstack service with configured port (defined in form of S3_ENDPOINT_URL=`http://localhost:4566`) to interact with.
2) For each bash terminal, before running any python code, use this command to retrieve values from `.env` and exporting them.
```
set -a
source .env
set +a
```
3) Create S3 localstack bucket with `create_bucket_localstack.py`. Bucket name chosen is `uk-house-price-localstack`
4) Ensure the bucket is successfully created with this command `awslocal s3 ls`
5) Run integration test with argument `region` if the prophet model for that region is already exist in `test_directory` , e.g. `python integration_test.py Oxford`. A prediction of `region` in parquet format (`Oxford_predictions.parquet`) will be uploaded to localstack bucket after having been generated in remote. Also, a snapshot of pandas loaded from parquet will appear in terminal.
6) Check whether the files have been successfully uploaded inside S3 localstack with command `awslocal s3 ls s3://uk-house-price-localstack --human-readable`

Update: Unit/integration testing, quality code rating, code formatting in automatic fashion is made possible with `Makefile`. Do the following:
1) Run the automated execution with command `make integration test` to run pytest in `tests` directory, quality check dictated by `isort`, `black`, and `pylint`. Lastly bash command in `run_test.sh` will generate docker image named `test_model` paired with tag `%Y-%m-%d-%H-%M-%S` that will be used for integration testing with AWS S3 localstack. 
2) Just follow steps from previous section except 1) (start from 2) all the way to 6))
3) After press `Ctrl+C` on running docker to stop localstack service
Before getting ready to push code to Github, check whether the code with `pre-commit`:
```
git init
pre-commit install

```
Pylint and black is used here for formatting. Both Pylint and black gives feedback on quality on the code is written.
Commands used (for demonstration) are `pylint baseline_learn.py` and `black --diff baseline_learn.py`.

## **Pre-Commit**

UK_house_price is set for pre-commit hooks.
