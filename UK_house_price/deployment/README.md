## **Deployment**

Model registry in MLFlow can then used later for deployment purpose. This section will cover the method of reusing model artifact stored in s3 bucket as a Prophet model that evaluates trend of house prices in a certain region. This programe is conducted in Flask environment.

### **Steps**
1) Set environment variables in bash terminal.
```
export RUN_ID="2a18236a06a346cd97a931f545d0be0f"
export REGION="Liverpool"
export S3_BUCKET="mlopszoomcamp-bucket"
```
3) Launch flask application with command `python deploy_mlflow.py`
4) See its response from flask with command `python deploy_test.py`

### **Deployment with Docker**
It is also possible to make a docker image for very same purpose. A little difference is that docker-compose will make use of environment variables defined in `.env` when starting the image. To make sure none of environment variables is active, run command:
```
unset RUN_ID
unset REGION
unset S3_BUCKET
```

1) Prepare required variables in `.env` then run command `docker build -t deployment_mlflow_flask .` inside `deployment` directory. The image should be built there.
2) Execute `docker-compose up` to start the image.
3) Execute `python deploy_test.py`
4) If you wish to change, stop the image with `docker-compose down` and replace values `RUN_ID` and `REGION` in `.env`. Then start the image again.
5) To avoid taking too much space, view image list with `docker image ls`. Running command `docker image rm <IMAGE ID>` will remove selected image.

