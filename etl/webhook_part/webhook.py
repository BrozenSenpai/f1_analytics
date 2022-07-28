import pymongo
from flask import Flask, request

from transform_load import (
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
        # get and insert seasons data
        get_seasons()
        # get and insert drivers data
        get_drivers()
        # get and insert drivers performance data
        get_drivers_performance()
        # get and insert drivers seasons data
        get_drivers_season_data()
        # get and insert constructors seasons data
        get_constructors_season_data()
        # get and insert races data
        get_races_data()
        # get and insert incidents data
        get_status_data()
        return "OK\n"


app.run(host="0.0.0.0", port=5010)
