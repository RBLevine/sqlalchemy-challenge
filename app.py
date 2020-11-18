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
        f"For start and end dates, the YYYY-MM-DD format must be used:<br/>"
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

@app.route("/api/v1.0/tobs")
def tobs():
    """Return dates and temp observations for 12 months from the most recent data point"""
   
    #Find the date of the last data point
    lastDataPoint = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    # Get the date of one year from the last data point
    oneYearBefore = dt.date(2017,8,23) - dt.timedelta(days=365)
 
    # Get the most active station - the station with the most data points
    stationCounts=session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    mostActiveID=stationCounts[0][0]

    # Get data and temp results for most active station
    mostActiveData = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == mostActiveID).filter(Measurement.date >=oneYearBefore).all()

    # Convert mostActiveData to dictionary where date is key and tobs in value
    mostActiveDict = {date: tobs for date, tobs in mostActiveData}

    return jsonify(mostActiveDict)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def date(start = None, end = None):
    """Return min temp, average temp, and max temp given a start date or date range."""

    # Get date and precipitation
    # If there is only a start date
    if end == None:
        minTemp = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start).scalar()
        maxTemp = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start).scalar()
        avgTemp = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start).scalar()
    
    # If there is a date range given
    else:
        minTemp = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).scalar()
        maxTemp = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).scalar()
        avgTemp = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).scalar()
    
    weatherDict = {}
    weatherDict["start_date"] = start
    weatherDict["end_date"] = end
    weatherDict["min_temp"] = minTemp
    weatherDict["max_temp"] = maxTemp
    weatherDict["avg_temp"] = avgTemp
    
    # Make sure information was available or return error message
    if minTemp == None or maxTemp == None or avgTemp == None:
        return "No temp data found for the date or range, please try a different date/range."
    
    else:
        return jsonify(weatherDict)

session.close()

if __name__ == '__main__':
    app.run(debug=True)