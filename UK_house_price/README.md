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

1) Baseline learning and [model_generation](https://github.com/rizdiaprilian/MLOps_Zoomcamp/blob/master/UK_house_price/baseline_learn.py)
2) [Baseline prediction](https://github.com/rizdiaprilian/MLOps_Zoomcamp/blob/master/UK_house_price/baseline_predict.py)

## **Experimentation**

The baseline workflow descripted above is then furtherly enhanced MLFlow paired with AWS EC2 and S3 that give the experiment degrees of reproducibility and greater range of tracking capability. Database to store information comprises of inference metrics and parameters is SQLite; Orchestration agent to manage of running smaller unit functions is Prefect Orion.

A file that covers tasks and flow of experimenting machine learning producing artifact prophet logs is presented [here](https://github.com/rizdiaprilian/MLOps_Zoomcamp/blob/master/UK_house_price/model_prefect.py)

## **Monitoring Strategy**
- Batch Monitoring: Predictions are generated in batch within specified interval, e.g. every six hours, every day, or monthly basis. Common use cases utilizing batch prediction includes collaborative filtering, content-based recommendations. Running app from prediction service sends input merged with generated output in JSON format to the Mongo DB. Data stored within MongoDB is transformed into pandas format and is compared with reference data loaded directly from csv file. A program incorporating prediction pipeline and drift calculation takes both reference and current data to be compared on the grounds of selected features with the use of `ColumnMapping`. The task is separably manageable on each running function with Prefect Orion.

- Online Monitoring: This service generates predictions after receiving requests. A downside is that the service needs to fulfill the requirement of running model in prolonged period until the change notice is issued.  

Since Evidently has yet released the feature specified for assessing time-series prediction, data drift is the only measurement to be covered in this section.

Prediction Service
