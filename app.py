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
engine = create_engine("sqlite:///./Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session
session=Session(engine)

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
        f"Welcome to the Hawaii Climate API! <br/>"
        f"Available Routes:<br/>"
        f"For dates and temp observations from the last year:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"List of all stations: <br/>"
        f"/api/v1.0/stations<br/>"
        f"Temp observations from the last year:<br/>"
        f"/api/v1.0/tobs<br/>"
        f"Min temp, average temp, and max temp for a given start date:<br/>"
        f"/api/v1.0/start<br/>"
        f"Min temp, average temp, and max temp for a given date range:<br/>"
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Query to retrieve precipitation data for 12 months since the last data point."""

    #Find the date of the last data point
    lastDataPoint = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    # Get the date of one year from the last data point
    oneYearBefore = dt.date(2017,8,23) - dt.timedelta(days=365)
    # Get the precipitation data
    PrecipData=session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= oneYearBefore).all()

    # Convert PrecipData to dictionary where date is the key and the prcp is the value
    PrecipDataDict = {date: prcp for date, prcp in PrecipData}

    return jsonify(PrecipDataDict)

@app.route("/api/v1.0/stations")
def stations():
    """Return JSON list of alll the stations in the dataset."""

    # Get the informatino for all stations
    stations = session.query(Station.station, Station.name, Station.elevation)

    # Convert stations into to dictionary
    stationDict = []
    for station, name, elevation in stations:
        station_dict = {}
        station_dict["elevation"] = elevation
        station_dict["name"] = name
        station_dict["station"] = station
        stationDict.append(station_dict)
    
    return jsonify(stationDict)
    


if __name__ == '__main__':
    app.run(debug=True)