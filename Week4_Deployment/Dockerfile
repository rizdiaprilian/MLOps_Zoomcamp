FROM python:3.9.7-slim

RUN pip install -U pip
RUN pip install pipenv 

WORKDIR /app

COPY [ "model.bin", "./" ]

##### Put new code below ######
##### Feel free to deactivate code ######



COPY [ "Pipfile", "Pipfile.lock", "./" ]

RUN pipenv install --system --deploy

COPY [ "starter_docker.py", "model.bin", "./" ]

EXPOSE 9696

ENTRYPOINT [ "gunicorn", "--bind=0.0.0.0:9696", "starter_docker:app" ]

#### docker build -t ride-duration-prediction-service:v1 .

#### docker run -it --rm -p 9696:9696 ride-duration-prediction-service:v1
