Here is a structure breakdown in files used to perform experimentation and orchestration:
- `baseline_learn.py` -> This script serves as learning baseline, including loading UK house price data and transforming it into format suitable for prophet model. Its output is a fitted model on specified region in bin format.  
- `baseline_predict.py` -> This script runs prediction on the unseen data and produces a parquet file that merges together observed rows with prediction result relative to the given date.
- `mlflow_experiment.ipynb` -> This notebook used as a starting point of bringing what has been laid in `baseline_learn.py` and `baseline_predict.py` to experimental settings powered by MLFlow, in which its functionalites allow developer to create snapshots (artifacts) of training and inference outputs generated from variations of input parameters. 
- `model_prefect.py` -> A modified version of `mlflow_experiment.ipynb` patched with decorators from Prefect Orion. Its resulting artifacts will be stored in S3 bucket while the information of metrics, tags and other input parameters are easily traceable in MLFlow environment.

A baseline workflow descripted above is furtherly enhanced by MLFlow paired with AWS S3 bucket that give the experiment degrees of reproducibility and greater range of tracking capability. Database to store information comprises of inference metrics and parameters is SQLite; Orchestration agent to monitor unit functions and workflow is Prefect Orion; it is a service that provide visual simulation that helps identify workflow coordination to then inform the data scientist about issues on functions when error arises.

Before working on this section, complete these pre-configurations below: 
1) Verify that a S3 bucket is already available before jumping to experimentation. This time `mlopszoomcamp-bucket` is chosen for bucket name.  
2) Confirm that aws configure has been set. Its record can be seen in `~/.aws/credentials`.

## **Fitting Prophet Model**

Prophet is used to capture forecasting capability on increasing trend of UK house price. Provided below are training and prediction at baseline stage.

1) Baseline learning and [model_generation](https://github.com/rizdiaprilian/MLOps_Zoomcamp/blob/master/UK_house_price/baseline_learn.py). This file will generate a model trained on a specified region after splitted under a given date and it is stored inside directory `models`. For example, command `python baseline_learn.py Oxford "2019-01-01"` will generate `models_prophet_Oxford.bin`
2) Then run the prediction on a selected region with [Baseline prediction](https://github.com/rizdiaprilian/MLOps_Zoomcamp/blob/master/UK_house_price/baseline_predict.py), e.g. `python baseline_predict.py Oxford "2019-01-01"`.

## **MLFlow Experimentation**

Experiment provided in jupyter notebook is named `UK_house_price_forecasting`. Launch jupyter lab with command `jupyter lab` and it will be appear in browser.

### **Steps**
1) Open [Jupyter Notebook](https://github.com/rizdiaprilian/MLOps_Zoomcamp/blob/master/UK_house_price/mlflow_experiment.ipynb). Run the very first cell after setting tracking server.

![image](https://user-images.githubusercontent.com/42743243/189531493-efdba89f-a4ca-43ab-91f4-2dccc5577aac.png)

Launch MLFlow with command `mlflow server -h 0.0.0.0 -p 5000 --backend-store-uri sqlite:///mlflow_uk_house.db --default-artifact-root s3://mlopszoomcamp-bucket`

![image](https://user-images.githubusercontent.com/42743243/187728007-28af1174-96ff-477c-ac7f-16f2cdb752ff.png)

Copy the output of that cell and paste it to the address bar to start MLFlow.

Alternatively, you can also launch MLFlow without needing to start jupyter lab. Use the command below and do the same thing on copy and paste tracking uri.
```
export MLFLOW_TRACKING_URI="http://ec2-3-11-9-244.eu-west-2.compute.amazonaws.com:5000"
mlflow ui -h 0.0.0.0 -p 5000 --backend-store-uri sqlite:///mlflow_uk_house.db \
        --default-artifact-root s3://mlopszoomcamp-bucket
```

2) Run the following command as follows to open Prefect Orion:
```
prefect config set PREFECT_ORION_UI_API_URL="<Public IPv4 address>/api"
prefect config set PREFECT_API_URL="<Public IPv4 address>/api"
prefect orion start --host 0.0.0.0
```

![image](https://user-images.githubusercontent.com/42743243/187728101-75ffe464-b34d-4c5a-8c24-15e7d93459e4.png)

3) Run the [prediction](https://github.com/rizdiaprilian/MLOps_Zoomcamp/blob/master/UK_house_price/model_prefect.py) with command `python model_prefect.py Oxford "2019-01-01"` generates an artifact with several logs along with parameters and forecasting metrics and the logged model can be used for deployment.
