## Create new model which directly populate items from s3 bucket
aws s3 cp --recursive s3://mlopszoomcamp-bucket/UK_house_price/{RUN_ID}/artifacts/models_prophet/ model