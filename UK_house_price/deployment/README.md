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
