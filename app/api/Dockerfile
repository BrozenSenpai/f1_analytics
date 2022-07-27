FROM python:3.10-slim-bullseye

WORKDIR /api

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY config.py server.py gunicorn_config.py entrypoint.sh ./

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["sh", "entrypoint.sh"]
