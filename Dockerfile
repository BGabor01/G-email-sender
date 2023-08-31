FROM python:3.11-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends git ca-certificates\
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* 

RUN update-ca-certificates

WORKDIR /app


RUN pip install --no-cache-dir pipenv


COPY Pipfile Pipfile.lock ./

RUN pipenv install --deploy --ignore-pipfile --system

COPY . .

CMD ["python", "main.py"]
