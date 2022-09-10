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

## **Project Structure**

This project is developed and tested using cloud service AWS. As such, any configuration made for running programs and services is adjusted to make full use of AWS services, with most of progrmas utilize S3 bucket mainly for storing and reproducing models after completing machine learning experiment.

Structures are constructed as follows:
- [deployment](https://github.com/rizdiaprilian/MLOps_Zoomcamp/tree/master/UK_house_price/deployment)
- [monitoring](https://github.com/rizdiaprilian/MLOps_Zoomcamp/tree/master/UK_house_price/monitoring_ML)
- [testing](https://github.com/rizdiaprilian/MLOps_Zoomcamp/tree/master/UK_house_price/test_directory)

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
4) Check whether python VSCode is inside pipenv with command `which python`

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


## **Pre-Commit**

To better identify simple, minor issues and make sure that testing runs well before submission to github, pre-commit hooks is configured for this project.

1) Inside `UK_house_price` initialize empty git with `git init`.
2) Create pre-commit yaml file with command `pre-commit sample-config > .pre-commit-config.yaml` 
3) Install pre-commit after `.git` appears in directory.
![image](https://user-images.githubusercontent.com/42743243/189482497-0402ad99-f447-434a-9851-74188d9b527e.png)
4) Generate `.gitignore` to exclude files/folders from hooks.
5) Add them with `git add <files/folders>`. You can also use `git rm --cached <files/folders>` if you wish to exclude some files and folders from testing hooks.
6) Command `git commit -m "<message>"` will show the process of fixing files (if there are sign of code issues detected)
![image](https://user-images.githubusercontent.com/42743243/189483558-370dc1b4-491f-4460-88d2-2a9a2dc11f7a.png)
![image](https://user-images.githubusercontent.com/42743243/189483596-6862bc98-ef17-4bde-a1be-6b867cc05e0f.png)
7) To see which files that receive fixing, go with command `git diff`. Press `Q` to exit from the command
8) repeat the process 5) and 6) and observe whether changes made on code pass all tests. 
9) View commit (if success) with `git log`
![image](https://user-images.githubusercontent.com/42743243/189483952-dcfd6999-50eb-4533-9664-1c751a4b7698.png)
10) Remove `.git` from directory with `rm -rf .git`.



