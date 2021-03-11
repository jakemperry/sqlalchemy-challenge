#Import python modules
import pandas as pd
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
        f"<br/>"
        f"Query for min, max, and average temperatures starting with a start date or between a start date and end date. <br/>"
        f"Dates must be in YYYY-MM-DD format.<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
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
        .filter(Measurement.date >= yearAgo)\
        .group_by(Measurement.date).all()

    #Close session!
    session.close()

    #Save results in a dictionary
    prcpDict = {}
    for date, prcp in lastYearPrecip:
       prcpDict[date] = prcp
    return jsonify(prcpDict)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    activeStations = session.query(Measurement.station, func.count(Measurement.date))\
    .group_by(Measurement.station)\
    .order_by(func.count(Measurement.date)\
    .desc()).all()

    session.close()

    return jsonify(activeStations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    mostRecentDate = session.query(Measurement.date) \
    .order_by(Measurement.date.desc()).first()

    # Starting from the most recent data point in the database. 
    mostRecentSplit = mostRecentDate[0].split("-")
    recentDate = dt.date(int(mostRecentSplit[0]),int(mostRecentSplit[1]),int(mostRecentSplit[2]))
    
    # Calculate the date one year from the last date in data set.
    yearAgo = recentDate - dt.timedelta(days=365)
    busyStation = session.query(Measurement.station, func.count(Measurement.date))\
        .filter(Measurement.date >= yearAgo)\
        .group_by(Measurement.station)\
        .order_by(func.count(Measurement.date)\
        .desc()).first()

    busyTOBS = session.query(Measurement.station, Measurement.date, Measurement.tobs)\
        .filter(Measurement.station == busyStation[0])\
        .filter(Measurement.date >= yearAgo).all()

    session.close()
    return jsonify(busyTOBS)

@app.route("/api/v1.0/<start>")
def dateSpan(start):
    startDate = start
    session = Session(engine)

    tmin = session.query(func.min(Measurement.tobs))\
        .filter(Measurement.date >= startDate).first()

    tmax = session.query(func.max(Measurement.tobs))\
        .filter(Measurement.date >= startDate).first()

    tavg = session.query(func.avg(Measurement.tobs))\
        .filter(Measurement.date >= startDate).first()
    session.close()

    resultDict = {"TMIN":tmin,
                    "TMAX":tmax,
                    "TAVG":tavg}
    return jsonify(resultDict)


@app.route("/api/v1.0/<start>/<end>")
def datesSpan(start, end):
    startDate = start
    endDate = end
    session = Session(engine)
    tmin = session.query(func.min(Measurement.tobs))\
        .filter(Measurement.date >= startDate)\
        .filter(Measurement.date <= endDate).first()

    tmax = session.query(func.max(Measurement.tobs))\
        .filter(Measurement.date >= startDate)\
        .filter(Measurement.date <= endDate).first()

    tavg = session.query(func.avg(Measurement.tobs))\
        .filter(Measurement.date >= startDate)\
        .filter(Measurement.date <= endDate).first()
    session.close()

    resultDict = {"TMIN":tmin,
                    "TMAX":tmax,
                    "TAVG":tavg}
    return jsonify(resultDict)

if __name__ == '__main__':
    app.run(debug=True)