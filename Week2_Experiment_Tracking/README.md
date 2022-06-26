# **Experiment Tracking**

This week we learn about managing machine learning information in various aspects: hyperparameter, metric, models, etc. MLFlow offers features that promotes reproducibility, organizing, and model optimization that helps us tracking variations in training and inference performance from many different parameters and retrieving saved model as needed without much of hassle.

### **MLFlow** 
![Image](https://github.com/rizdiaprilian/MLOps_Zoomcamp/blob/master/Week2_Experiment_Tracking/MLFlow_screenshot.png)

Ways to start MLFlow UI in Terminal:
1) With SQLite
`mlflow ui --backend-store-uri sqlite:///mlflow.db`

an instance database file named `mlflow.db` will appear inside the directory that mlflow ui starts
