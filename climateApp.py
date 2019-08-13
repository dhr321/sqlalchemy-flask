import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations</br>"
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/20160823</br>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all Measurement
    start_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    end_date = dt.date(2017,8,23)
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= start_date).\
    filter(Measurement.date <= end_date).all()

    session.close()

    # Convert list of tuples into normal list
    # all_precip = list(np.ravel(results))
    all_precip = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict[date] = prcp
        all_precip.append(precip_dict)
    return jsonify(all_precip)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all passengers
    results = session.query(Measurement.station, func.count(Measurement.id)).\
        group_by(Measurement.station).order_by(func.count(Measurement.id).desc()).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_stations = []
    for station in results:
        station_dict = {}
        station_dict["station"] = station
        all_stations.append(station_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all observed temps for specified time period.
    start_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    end_date = dt.date(2017,8,23)
    results = session.query(Measurement.tobs).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).\
        filter(Measurement.station == 'USC00519281').\
        all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_tobs = []
    for tobs in results:
        tobs_dict = {}
        tobs_dict["observedTemp"] = tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

@app.route("/api/v1.0/start")
def start():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all observed temps for specified time period.
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), \
        func.avg(Measurement.tobs)).\
        filter(Measurement.station == 'USC00519281').all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_starts
    all_starts = []
    start_dict = {}
    start_dict["tmin"] = results[0]
    start_dict["tmax"] = results[1]
    start_dict["tave"] = results[2]
    all_starts.append(start_dict)

    return jsonify(all_starts)

"""
if __name__ == '__main__':
    app.run(debug=True)
"""