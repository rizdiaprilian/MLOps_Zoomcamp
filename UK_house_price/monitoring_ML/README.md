## **Monitoring Prediction**

This step will bring further the model to be able to respond from given request in environment: deployment.

- Batch Monitoring: Predictions are generated in batch within specified interval, e.g. every six hours, every day, or monthly basis. Common use cases utilizing batch prediction includes collaborative filtering, content-based recommendations. Running app from prediction service sends input merged with generated output in JSON format to the Mongo DB. Data stored within MongoDB is transformed into pandas format and is compared with reference data loaded directly from csv file. A program incorporating prediction pipeline and drift calculation takes both reference and current data to be compared on the grounds of selected features with the use of `ColumnMapping`. The task is separably manageable on each running function with Prefect Orion.

- Online Monitoring: This service generates predictions after receiving requests. A downside is that the service needs to fulfill the requirement of running model in prolonged period until the change notice is issued.

Since Evidently has yet released the feature specified for assessing time-series prediction, data drift is the only measurement to be covered in this section. Both online and batch monitors are used in this project. This directory is contained as defined in `docker-compose.yml`. You may launch the following command that will start prediction service along with MongoDB, Grafana, Evidently.

### **Prediction Service**
This service generates predictions on requested rows delivered by`send_data.py` and submit them to Evidently and MongoDB.  

![image](https://user-images.githubusercontent.com/42743243/187480203-91ea5fdd-1b90-4f3d-8e5c-f698453de426.png)

### **MongoDB**

The MongoDB serves a purpose to save the prediction record generated for responding the requests delivered from `send_data.py` that is merged with input record. Example of showing the prediction result in Pandas format is provided here.

### **Evidently**
Evidently will open two different data: reference and prediction. Reference is directly from dataset csv while the prediction is loaded in JSON format. Comparison will take place on these two after the prediction is transformed into Pandas Dataframe.

### **Running Services with Docker**

Inside directory `monitoring_ML`, do:
1) Prepare three bash terminals, in which these terminals are used to: operate services with Docker compose, send data to MongoDB and Evidently, and generate data drift report.
2) Execute `docker-compose up` to start up service as follows: Prometheus, Grafana, MongoDB, and Evidently.
3) Login Grafana with the same value for username and password: `admin`.
4) Run 'python send_data.py` to start sending data to MongoDB and Evidently monitoring service. An example of data drift monitoring in Grafana appears to be shown below
![image](https://user-images.githubusercontent.com/42743243/189478584-7df0ba1e-beef-4b59-afc0-70dad79f555c.png)
![image](https://user-images.githubusercontent.com/42743243/189479026-1fd76174-697c-4b57-99f0-94236c6f62fa.png)


5) Run 'python prefect_batch_monitoring.py' to produce a summary of data drift in HTML format. As this [file](https://github.com/rizdiaprilian/MLOps_Zoomcamp/blob/master/UK_house_price/monitoring_ML/evidently_report_UK_house_price.html) size is too large for viewing, it is recommended to download first and open it in browser. 
![image](https://user-images.githubusercontent.com/42743243/189478594-326ecf97-0cef-484c-a3b7-b6992c5ec250.png)
6) If you wish to stop the service, just run `docker-compose down`.
7) To avoid taking too much space, view image list with `docker image ls`. Running command `docker image rm <IMAGE ID>` will remove selected image.
