# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify



#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement 
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

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
    return (f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/start<br/>"
            f"/api/v1.0/start/end"
    )        


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    one_year_ago=dt.date(2017,8,23)-dt.timedelta(days=365)

    
    results=session.query(measurement.date, measurement.prcp).\
    filter(measurement.date>=one_year_ago).all()

    session.close()
    all_precipitation_data=[]
    for date, prcp, in results:
        prcp_dict = {}
        
        prcp_dict["date"] = date
        prcp_dict["precipitation"] = prcp
        all_precipitation_data.append(prcp_dict)

    return jsonify(all_precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
   
    second_results=session.query(Station.station,Station.name).all()

    session.close()

    station_data=[]
    for station, id in second_results:
        station_dict={}
        station_dict['station']= station
        station_dict['name']= id 

        station_data.append(station_dict)
    return jsonify(station_data)
    
@app.route("/api/v1.0/tobs")
def tobs():
    session=Session(engine)

    one_year_ago=dt.date(2017,8,23)-dt.timedelta(days=365)

    
    results=session.query(measurement.date, measurement.tobs).\
    filter(measurement.date>=one_year_ago).\
    filter(measurement.stations=='USC00519281').all()
    session.close()
    all_tobs_data=[]
    for date, tobs, in results:
        tobs_dict = {}
        
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        all_tobs_data.append(tobs_dict)

    return jsonify(all_tobs_data)

@app.route("/api/v1.0/<start>")
def start(start):
    session = session(engine)
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")
    start_date_results=session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
    filter(measurement.date>=start_date).all()
    session.close()

    start_data=[]
    for min, max, avg in start_date_results:
        start_date_dict={}
        start_date_dict["min"]=min
        start_date_dict["max"]=max
        start_date_dict["avg"]=avg
        start_data.append(start_date_dict)

    return jsonify(start_data)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start,end):
    session=session(engine)
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")
    end_date = dt.datetime.strptime(end, "%Y-%m-%d")
    start_end_date_results=session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
    filter(measurement.date>=start_date).filter(measurement.date<=end_date).all()
    session.close()
    start_end_data=[]
    for min, max, avg in start_end_date_results:
        start_end_date_dict={}
        start_end_date_dict["min"]=min
        start_end_date_dict["max"]=max
        start_end_date_dict["avg"]=avg
        start_end_data.append(start_end_date_dict)

    return jsonify(start_end_data)

if __name__=='_main_':
    app.run(debug=True)