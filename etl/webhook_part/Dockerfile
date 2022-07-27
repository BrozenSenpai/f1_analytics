FROM python:3.10-slim-bullseye

WORKDIR /etl

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY config.py utils.py data_wrangle.py webhook.py ./

ENTRYPOINT ["python", "webhook.py"]
