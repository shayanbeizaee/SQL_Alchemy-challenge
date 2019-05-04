#Shayan Beizaee

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime
import pandas as pd
import datetime as dt

from flask import Flask, jsonify

from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = automap_base()  

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement

app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Welcome to my climate app!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    date_in = dt.datetime(2016, 8, 23)
    last_12prcp = db_session.query(Measurement.date,Measurement.prcp).filter(Measurement.date > date_in).order_by(Measurement.date.asc()).all()

    return jsonify(last_12prcp)

@app.route("/api/v1.0/stations")
def station():

    stationz = db_session.query(Measurement.station).group_by(Measurement.station).all()
    return jsonify(stationz)
    
@app.route("/api/v1.0/tobs")
def temp():

    date_in = dt.datetime(2016, 8, 23)
    temp_station = db_session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > date_in).all()
    return jsonify(temp_station)

@app.route("/api/v1.0/<start>")
def result(start):

     answer = db_session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).group_by(Measurement.date).all()
     return jsonify(answer)

@app.route("/api/v1.0/<start>/<end>")
def results(start, end):

    start_end = db_session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(Measurement.date).all()
    return jsonify(start_end)