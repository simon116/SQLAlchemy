######################################################################
# Imports
from flask import Flask, jsonify

# Add everything from JN
import numpy as np
import pandas as pd
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Set up Flask
app = Flask(__name__)

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite") # change this to your file path
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)

######################################################################
# Routes

@app.route('/')
def home():
  return (
    f"Welcome to my weather page!<br/>"
    f"Routes:<br/>"
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/start and /api/v1.0/start/end<br/>"
  )

# precipitation route
@app.route('/api/v1.0/precipitation')
def precip():
  query_results = session.query(Measurement.date, Measurement.prcp)
  precipitation_data = query_results.all()

  return jsonify(precipitation_data)

@app.route('/api/v1.0/stations')
def station_query():
  # Design a query to show how many stations are available in this dataset?
  session.query(func.count(Station.station)).all()

  station_counts = (session.query(Measurement.station, func.count(Measurement.station))
                        .group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all())
  
  print(station_counts)
  
  return jsonify(station_counts)


# temperature observed route
@app.route('/api/v1.0/tobs')
def tobs():
  tobs_data = (session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= '2016-08-23')
                   .filter(Measurement.station == 'USC00519281').order_by(Measurement.date).all())

  return jsonify(tobs_data)

@app.route('/api/v1.0/<start>')
def temperature_start(start=None):
  print('start date:', start)

  temp_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

  return jsonify(temp_data)

@app.route('/api/v1.0/<start>/<end>')
def temperature_start_end(start=None, end=None):
  print('start date:', start)
  print('end date:', end)

  temp_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

  return jsonify(temp_data)

# Run app
if __name__ == '__main__':
    app.run()