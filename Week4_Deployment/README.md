# **ML Deployment**

So far, we have managed to register machine learning with MLFlow that makes it easier to reproduce the model later as well as writing orchestration script in Prefect to render the model suitable for production. This step will bring further the model to be able to respond from given request in environment: deployment.

Setup preparation for model deployment can be done either in batch (offline) that allow prediction on newly unseen data arrives in periodic schedule or in real-time streaming (online) that the model always runs to serve anytime. 

## **Web-service Deployment**

This section covers the usage of python environment in `pipenv` that greatly manage packages as defined in `Pipfile`. `Pipfile.lock` is generated when creating a new environment that produce deterministic builds.

An example of lists of packages can be seen [here](https://github.com/rizdiaprilian/MLOps_Zoomcamp/blob/master/Week4_Deployment/Pipfile), in which are ready for installation. 

### Pipenv Installation

- move to a folder that stores `Pipfile` and write: `pipenv install scikit-learn==1.0.2 flask --python=3.9`

- You can also add other packages in `Pipfile` later on. Be sure that the version used for programming stays the same to the version for deployment.

- Command used for checking version: `pip freeze | grep scikit-learn` and `python --version`

- Activate pipenv environment with this command `pipenv shell` then `PS1="> "` to make the prompt shorter.

Information about pipenv: https://pipenv.pypa.io/en/latest/

### Prediction in Local Machine

- Prepare a script that read data from online repository and load DictVectorizer and LinearRegression defined in `model.bin`as stated in [here](https://github.com/rizdiaprilian/MLOps_Zoomcamp/blob/master/Week4_Deployment/starter.py).
- Run command that takes `year` and `month` as input argument of `main()`. For example `python starter.py 2021 10`. Observe the output coming from running the command.

### Prediction in Flask

Modify `starter.py` compatible to web service that interacts with HTTP endpoint.

## **Streaming Deployment**
