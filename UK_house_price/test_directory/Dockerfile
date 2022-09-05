FROM python:3.9.12-slim

RUN pip install -U pip
RUN pip install pipenv 

WORKDIR /app

COPY [ "Pipfile", "Pipfile.lock", "./" ]

RUN pipenv install --system --deploy

COPY [ "integration_test.py", "integration_test.py" ]
COPY [ "model_prophet_Oxford.bin", "model_prophet_Oxford.bin" ]

# CMD ["pipenv shell"]

ENTRYPOINT [ "python", "integration_test.py" ]