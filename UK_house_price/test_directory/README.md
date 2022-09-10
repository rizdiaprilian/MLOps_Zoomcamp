## **Testing**

We wish to test how well the prediction works. AWS S3 localstack and Docker is used to serve this purpose. Again `.env` is provided to give environment variables for helping testing codes more loosely coupled.

1) Build docker inside `test_directory` as specified in `run_test.sh`. Then execute `docker-compose up` that will launch localstack service with configured port (defined in form of S3_ENDPOINT_URL=`http://localhost:4566`) to interact with.
2) For each bash terminal, before running any python code, use this command to retrieve values from `.env` and exporting them.
```
set -a
source .env
set +a
```
3) Create S3 localstack bucket with `create_bucket_localstack.py`. Bucket name chosen is `uk-house-price-localstack`
![image](https://user-images.githubusercontent.com/42743243/189481667-8a80eb75-962f-476b-8d18-2124b5efc5c6.png)

4) Ensure the bucket is successfully created with this command `awslocal s3 ls`
![image](https://user-images.githubusercontent.com/42743243/189481690-5cc02288-24f1-44eb-9890-9d8db3da44c5.png)

5) Run integration test with argument `region` if the prophet model for that region is already exist in `test_directory` , e.g. `python integration_test.py Oxford`. A prediction of `region` in parquet format (`Oxford_predictions.parquet`) will be uploaded to localstack bucket after having been generated in remote. Also, a snapshot of pandas loaded from parquet will appear in terminal.
![image](https://user-images.githubusercontent.com/42743243/189481701-03bf29d1-2a54-4e8a-9d60-2e6709f7a350.png)

6) Check whether the files have been successfully uploaded inside S3 localstack with command `awslocal s3 ls s3://uk-house-price-localstack --human-readable`
![image](https://user-images.githubusercontent.com/42743243/189481711-70884325-9644-40a1-bfb5-8d39d9e54a81.png)

Update: Unit/integration testing, quality code rating, code formatting in automatic fashion is made possible with `Makefile`. Do the following:
1) Run the automated execution with command `make integration test` to run pytest in `tests` directory, quality check dictated by `isort`, `black`, and `pylint`. Lastly bash command in `run_test.sh` will generate docker image named `test_model` paired with tag `%Y-%m-%d-%H-%M-%S` that will be used for integration testing with AWS S3 localstack. 
![image](https://user-images.githubusercontent.com/42743243/189481631-4db99f50-83fc-4741-9800-6a569569e73c.png)
![image](https://user-images.githubusercontent.com/42743243/189481643-b0f8bb2c-9d06-4b7c-9203-458e640719b1.png)
![image](https://user-images.githubusercontent.com/42743243/189481650-30f4f622-d6ed-4f72-b530-3d35e37b02b9.png)

2) Just follow steps from previous section except 1) (start from 2) all the way to 6))
3) After press `Ctrl+C` on running docker to stop localstack service.
