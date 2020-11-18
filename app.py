import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt
from dateutil.relativedelta import relativedelta


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