import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup

engine = create_engine("sqlite:///Resources/hawaii.sqlite",connect_args={'check_same_thread': False})

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################

# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
         f"Avalable Routes:<br/>"
         
         f"/api/v1.0/precipitation<br/>"
         f"- Dates and Temperature Observations from last year<br/>"
         
         f"/api/v1.0/stations<br/>"
         f"- List of weather stations from the dataset<br/>"

         f"/api/v1.0/tobs<br/>"
         f"- List of temperature observations (tobs) from the previous year<br/>"

         f"/api/v1.0/<start><br/>"
         f"- List of min, avg, and max temperature for a given start date<br/>"
        
         f"/api/v1.0/<start>/<end><br/>"
         f"- List of min, avg, and max temperature for a given start/end range<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of precipitations from last year"""
    # Calculate the date 1 year ago from the last data point in the database
    date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    latest_date = dt.datetime(2017,8,23)
    year_ago = latest_date - dt.timedelta(days=365)

    # Design a query to retrieve the last 12 months of precipitation data and plot the results
    prcp_results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()

    # Convert the query results to a Dictionary using date as the key and prcp as the value
    prcp_all = []
    for result in prcp_results:
        prcp_dict = {}
        prcp_dict["date"] = prcp_results[0]
        prcp_dict["prcp"] = float(prcp_results[1])

        prcp_all.append(prcp_dict)

    return jsonify(prcp_all)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations"""
    # Design a query to return list of stations from dataset
    stations_results = session.query(Station.station).all()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(stations_results))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    """Return a JSON list of Temperature Observations (tobs) for the previous year."""
    # Calculate the date 1 year ago from the last data point in the database
    date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    latest_date = dt.datetime(2017,8,23)
    year_ago = latest_date - dt.timedelta(days=365)

    # Design a query to retrieve the last 12 months of temperatures
    tobs_results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= year_ago).all()

    # Convert list of tuples into normal list
    tobs_list = list(tobs_results)

    return jsonify(tobs_list)


@app.route("/api/v1.0/<start>")
def start_date(start=None):
    """Return a JSON list of tmin, tmax, tavg for the dates greater than or equal to the date provided"""
    start = dt.datetime.strptime(start, '%Y-%m-%d').date()
    start_results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).all()

    # Convert list of tuples into normal list
    start_list = list(np.ravel(start_results))
    return jsonify(start_list)


@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start=None, end=None):
    """Return a JSON list of tmin, tmax, tavg for the dates greater than or equal to the date provided"""
    start = dt.datetime.strptime(start, '%Y-%m-%d').date()
    end = dt.datetime.strptime(end, '%Y-%m-%d').date()
    start_end_results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    # Convert list of tuples into normal list
    start_end_list = list(np.ravel(start_end_results))
    return jsonify(start_end_results)


if __name__ == '__main__':
    app.run(debug=True)