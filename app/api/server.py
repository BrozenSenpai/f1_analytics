from flask import Flask, jsonify
from pymongo import MongoClient

from config import mongo_access

app = Flask(__name__)


client = MongoClient(mongo_access)
db = client.f1db


# create endpoint for seasons data
@app.route("/api/seasons", methods=["GET"])
def seasons():
    table = db.seasons
    return jsonify(list(table.find({}, {"_id": False})))


# create endpoint for drivers data
@app.route("/api/drivers", methods=["GET"])
def drivers():
    table = db.drivers
    return jsonify(list(table.find({}, {"_id": False})))


# create endpoint for drivers seasons data
@app.route("/api/drivers_seasons/<string:season>", methods=["GET"])
def drivers_seasons(season):
    table = db.drivers_seasons
    return jsonify(list(table.find({"Season": season}, {"_id": False})))


# create endpoint for constructors seasons data
@app.route("/api/constructors_seasons/<string:season>", methods=["GET"])
def constructors_seasons(season):
    table = db.constructors_seasons
    return jsonify(list(table.find({"Season": season}, {"_id": False})))


# create endpoint for races data
@app.route("/api/races/<string:season>", methods=["GET"])
def races(season):
    table = db.races
    return jsonify(list(table.find({"Season": season}, {"_id": False})))


# create endpoint for incidents data
@app.route("/api/incidents/<string:season>", methods=["GET"])
def incidents(season):
    table = db.incidents
    return jsonify(list(table.find({"Season": season}, {"_id": False})))


# create endpoint for drivers performance data
@app.route("/api/drivers_performance/<string:driver>", methods=["GET"])
def drivers_performance(driver):
    table = db.drivers_performance
    return jsonify(list(table.find({"Driver": driver}, {"_id": False})))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011)
