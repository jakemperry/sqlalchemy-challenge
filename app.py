#Import python modules
import pandas as pd
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#Setup Database
engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

#Setup Flask
app = Flask(__name__)

#Flask routes

@app.route("/")
def homepage():
    return (
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    mostRecentDate = session.query(Measurement.date) \
    .order_by(Measurement.date.desc()).first()

    # Starting from the most recent data point in the database. 
    mostRecentSplit = mostRecentDate[0].split("-")
    recentDate = dt.date(int(mostRecentSplit[0]),int(mostRecentSplit[1]),int(mostRecentSplit[2]))
    
    # Calculate the date one year from the last date in data set.
    yearAgo = recentDate - dt.timedelta(days=365)
    
    # Perform a query to retrieve the data and precipitation scores
    lastYearPrecip = session.query(Measurement.date, func.sum(Measurement.prcp))\
        .filter(Measurement.date >= yearAgo).group_by(Measurement.date).all()

    #Close session!
    session.close()

    #Save results in a dictionary
    prcpDict = {}
    for date, prcp in lastYearPrecip:
       prcpDict[date] = prcp
    return prcpDict 

if __name__ == '__main__':
    app.run(debug=True)