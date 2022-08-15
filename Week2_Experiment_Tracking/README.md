# **Experiment Tracking**

This week we learn about managing machine learning information in various aspects: hyperparameter, metric, models, etc. MLFlow offers features that promotes reproducibility, organizing, and model optimization that helps us tracking variations in training and inference performance from many different parameters and retrieving saved model as needed without much of hassle.

### **MLFlow** 
![Image](https://github.com/rizdiaprilian/MLOps_Zoomcamp/blob/master/Week2_Experiment_Tracking/MLFlow_screenshot.png)

Ways to start MLFlow UI in local machine:
1) With SQLite in local machine
`mlflow ui --backend-store-uri sqlite:///mlflow.db`

2) With PostgreSQL in AWS linux environment:
`mlflow server -h 0.0.0.0 -p 5000 --backend-store-uri postgresql://<db name>:<unique-id>@<url>:5432/<db name> --default-artifact-root <s3 bucket>`


See documentation here: https://www.mlflow.org/docs/latest/index.html
