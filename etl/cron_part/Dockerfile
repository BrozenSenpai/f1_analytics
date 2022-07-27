FROM debian:bullseye-slim

RUN apt-get update && apt-get install curl cron unzip sqlite3 -y

WORKDIR /etl

COPY checker.sh entrypoint.sh ./

RUN chmod +x checker.sh entrypoint.sh

COPY cronjobs /etc/cron.d/cronjobs

RUN chmod 0644 /etc/cron.d/cronjobs

RUN crontab /etc/cron.d/cronjobs

ENTRYPOINT ["sh", "entrypoint.sh"]