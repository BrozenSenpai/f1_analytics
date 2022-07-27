# F1 Analytics

## Overview
The F1 Analytics is a portfolio project in the fields of data engineering and data visualization. The main goal of this project is to create a simple site for Formula 1 historical statistics overview, powered by data from [Ergast](https://ergast.com/mrd/) - an experimental web service that provides a historical record of motor racing data for non-commercial purposes. The second goal is just learning. 

## General architecture
![architecture](https://user-images.githubusercontent.com/41913470/181354247-365c4b79-042f-49bd-8b07-96003900ec15.png)

The Ergast provides provide the data in the API and also a database images or CSV files form. This project uses files mainly because I have already created the [project](https://github.com/BrozenSenpai/yukinator) about the Ergast API. The second thing is that Ergast provides the data mostly for analytical purposes. It would be quite unfair to use their servers for my web app. To obtain the data files and store them in the SQLite3 database the bash script is running every 12 AM/PM (scheduled with CRON). It also checks if the data is updated, if so it sends the POST request to the webhook, which transforms the required data and upserts it into MongoDB. The data in the optimal form is served via API and accessed by a web app created with Dash. The WSGI Server used is the Gunicorn with 2 workers and 2 threads. The whole project is containerized using Docker with docker-compose.

## Tools
The following tools and technologies are used:
* **Python** - main programming language
* **Bash** - for shell commands and scripting
* **Cron** - for scheduling
* **Sqlite** - main relational database
* **MongoDB** - main document-oriented database
* **Flask** - for webhook and API
* **Dash** - for web app
* **Gunicorn** - WSGI server
* **Docker** - for containerization

## Steps to reproduce
To run this repo locally follow the steps listed below.

### Part 1
Install and configure docker + docker_compose.

### Part 2
In the directory top-most directory create *.env* file:
```bash
touch .env
```
Assing the following environment variables in the *.env*:
```
ROOT_NAME=<admin user name>
ROOT_PASSWORD=<admin user password>
DB_NAME=<name of database to create e.g. formula1db>
DB_USER=<name of user that will perform read and write operations>
DB_PASSWORD=<password of that user>
MONGO_ACCESS<url for authenticating with db, e.g. mongodb://db_user:db_password@mongodb:27017/formula1db> 
````
### Part 3
From the top-most directory run:
```bash
docker-compose up -d
```
The web app should be running on http://localhost:5012 (wait a 70 sec until the data is processed - sleep time can be changed in the  entrypoint).

### Part 4
To temporary shut down the containers run:
```bash
docker-compose down
```
To completely remove the project (including images and volumes) run:
```bash
docker-compose down --rmi all -v
```
**Warning**
This docker-compose is not production ready. Before running it in the production environment please take care of the security.
##
