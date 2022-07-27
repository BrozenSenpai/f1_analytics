FROM python:3.10-slim-bullseye

WORKDIR /web

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY tabs tabs/

COPY app.py components.py index.py gunicorn_config.py entrypoint.sh ./

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["sh", "entrypoint.sh"]