# **Monitoring Prediction**

This step will bring further the model to be able to respond from given request in environment: deployment.

Setup preparation for model deployment can be done either in batch (offline) that allow prediction on newly unseen data arrives in periodic schedule or in real-time streaming (online) that the model always runs to serve anytime. 

This directory is contained as defined in `docker-compose.yml`. You may launch the following command that will start prediction service along with MongoDB, Grafana, Evidently.

## **Prediction Service**
This service generates predictions on requested rows delivered by`send_data.py` and submit them to Evidently and MongoDB.  

![image](https://user-images.githubusercontent.com/42743243/187480203-91ea5fdd-1b90-4f3d-8e5c-f698453de426.png)

## **MongoDB**

The MongoDB serves a purpose to save the prediction record generated for responding the requests delivered from `send_data.py` that is merged with input record. Example of showing the prediction result in Pandas format is provided here.

## **Evidently**
Evidently will open two different data: reference and prediction. Reference is directly from dataset csv while the prediction is loaded in JSON format. Comparison will take place on these two after the prediction is transformed into Pandas Dataframe.