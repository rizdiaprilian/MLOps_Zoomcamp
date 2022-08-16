# **Experiment Tracking**

This week we learn about managing machine learning information in various aspects: hyperparameter, metric, models, etc. MLFlow offers features that promotes reproducibility, organizing, and model optimization that helps us tracking variations in training and inference performance from many different parameters and retrieving saved model as needed without much of hassle.

### **MLFlow** 
![Image](https://github.com/rizdiaprilian/MLOps_Zoomcamp/blob/master/Week2_Experiment_Tracking/MLFlow_screenshot.png)

Ways to start MLFlow UI in local machine:
1) With SQLite in local machine
`mlflow ui --backend-store-uri sqlite:///mlflow.db`

2) With SQLite in AWS linux environment
- in Jupyter notebook, run this command:
```
os.environ["AWS_PROFILE"] = "yourprofile" ## you have to set your own profile in ~/.aws/configure 

TRACKING_SERVER_HOST = "your Public IPv4 DNS" # fill in with the public DNS of the EC2 instance
mlflow.set_tracking_uri(f"http://{TRACKING_SERVER_HOST}:5000")
```
- in bash, run this command:
`mlflow server -h 0.0.0.0 -p 5000 --backend-store-uri sqlite://<db name> --default-artifact-root <s3 bucket>`

- back to Jupyter notebook, run this command: 
print(f"tracking URI: '{mlflow.get_tracking_uri()}'")
copy the link to the browser and paste it. MLflow would be loaded as shown below:
![image](https://user-images.githubusercontent.com/42743243/184874471-0d741216-5ca9-4296-a625-9d1308b4726b.png)


See documentation here: https://www.mlflow.org/docs/latest/index.html
