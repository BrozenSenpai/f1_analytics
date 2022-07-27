import pymongo
from flask import Flask, request

from utils import mongo_config, bulk_insert

from data_wrangle import (
    get_drivers_performance,
    get_drivers_season_data,
    get_constructors_season_data,
    get_races_data,
    get_status_data,
    get_seasons,
    get_drivers,
)

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():
    if request.json["message"] == "ready to serve":
        # set connection with MongoDB
        db = mongo_config()
        # get and insert drivers performance data
        drivers_performance = get_drivers_performance()
        bulk_insert(drivers_performance, db.drivers_performance)
        # get and insert drivers seasons data
        drivers_seasons = get_drivers_season_data()
        bulk_insert(drivers_seasons, db.drivers_seasons)
        # get and insert constructors seasons data
        constructors_seasons = get_constructors_season_data()
        bulk_insert(constructors_seasons, db.constructors_seasons)
        # get and insert races data
        races = get_races_data()
        bulk_insert(races, db.races)
        # get and insert incidents data
        status = get_status_data()
        bulk_insert(status, db.incidents)
        # get and insert max season data
        seasons = get_seasons()
        bulk_insert(seasons, db.seasons)
        drivers = get_drivers()
        bulk_insert(drivers, db.drivers)
        return "OK\n"


app.run(host="0.0.0.0", port=5010)
