import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


engine = create_engine("sqlite:///hawaii.sqlite")
app = Flask(__name__)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Stations = Base.classes.hawaii_stations
Measurement = Base.classes.hawaii_measurements


@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"api/v1.0/tobs"
        f"/api/v1.0/<start"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def prcp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all Datas and Prcp levels"""
    # Query all Dates
    results = session.query(Measurement.date).all()

    session.close()

    prcp_results = session.query(Measurement.prcp).all()

    # Convert list of tuples into normal list
    all_dates = list(np.ravel(results))
    all_prcp = list(np.ravel(prcp_results))

    return jsonify(all_dates, all_prcp)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all Datas and Prcp levels"""
    # Query all Stations
    stations = session.query(Stations.datestation).all()

    session.close()


    # Convert list of tuples into normal list
    all_stations = list(np.ravel(stations))

    return jsonify(all_stations)


@app.route("api/v1.0/tobs")

def tobs():
    session = Session(engine)
    tobs_stations_results = session.query(Measurement.station).all()
    session.close()

    tobs_results = session.query(Measurement.tobs).all()

    all_tobs_stations = list(np.ravel(tobs_stations_results))
    tobs_results = list(np.ravel(tobs_results))

    return jsonify(all_tobs_stations, tobs_results)


@app.route("/api/v1.0/<start")

def start_temps(start_date):
    session = Session(engine)
  
    start_date = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    
    start_results = list(np.ravel(start_date))

    return jsonify(start_results)



@app.route("/api/v1.0/<start>/<end")

def calc_temps(start_date, end_date):
    session = Session(engine)
  
    start_end_date = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    start_end_results = list(np.ravel(start_end_date))

    return jsonify(start_end_results)