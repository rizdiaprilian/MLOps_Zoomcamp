### Before running Prefect Orion, set two configurations that matches with current IP address
prefect config set PREFECT_ORION_UI_API_URL="http://3.8.10.146:4200/api"

prefect config set PREFECT_API_URL="http://3.8.10.146:4200/api"

### You can run Prefect Orion after getting done above
prefect orion start --host 0.0.0.0

### Do this after setting mlflow.set_tracking_uri(f"http://{TRACKING_SERVER_HOST}:5000")
### Specifically for project UK_house_price
mlflow server -h 0.0.0.0 -p 5000 --backend-store-uri sqlite:///mlflow_uk_house.db --default-artifact-root s3://mlopszoomcamp-bucket

### Chance Public IP4v address each time EC2 runs each time
http://ec2-3-8-10-146.eu-west-2.compute.amazonaws.com:5000

export MLFLOW_TRACKING_URI="http://ec2-3-8-10-146.eu-west-2.compute.amazonaws.com:5000"

### Alternatively start mlflow with this command 
mlflow ui -h 0.0.0.0 -p 5000 --backend-store-uri sqlite:///mlflow_uk_house.db \
        --default-artifact-root s3://mlopszoomcamp-bucket