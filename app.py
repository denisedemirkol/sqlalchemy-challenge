import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta
import pandas as pd



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
Station     = Base.classes.station

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
    
    
    return(
        f"<p>Hawaii Weather API 1.0</p>"
        f"<p>List all available api routes:</p>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/stdate<br/>"
        f"/api/v1.0/start_date/end_date<br/>"
    )


    
# ************* precipitation *********************

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)


    """Return a list of precipitation"""
    # Query all measurements
    results = session.query(Measurement.date, Measurement.prcp ).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_measurements
    all_measurements = []
    for date, prcp in results:
        measurements_dict = {}
        measurements_dict["date"] = date        
        measurements_dict["precipitation"] = prcp
        
        all_measurements.append(measurements_dict)

    return jsonify(all_measurements)



# ************* Stations *********************

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)


    """Return a list of stations"""
    # Query all stations
    results = session.query(Station.id, Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation ).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_stations
    all_stations = []
    for id, station, name, latitude, longitude, elevation in results:
        station_dict = {}
        station_dict["id"] = id        
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        
        all_stations.append(station_dict)

    return jsonify(all_stations)


# ************* Tobs *********************

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    for u in session.query(Measurement.date).order_by(Measurement.date.desc()).first():    
        enddate = u
        #row is converted to string


    datetime_object = datetime.strptime(enddate, '%Y-%m-%d')
    print(f'Last data point is : {datetime_object}')

    yr_ago = datetime_object - relativedelta(years=1)
    print(f'A year ago is : {yr_ago}')


    sel = [Measurement.date, Measurement.tobs, Measurement.station]

    
    results = session.query(*sel).filter(Measurement.station == Station.station).\
                                  filter(Measurement.date >= yr_ago).all()



    session.close()

    all_tobs = []
    for date, tobs, station in results:
        #print(tobs)
        
        xx_dict = {}
        xx_dict["station"] = station        
        xx_dict["date"] = date        
        xx_dict["tobs"] = tobs

        print(xx_dict)
        all_tobs.append(xx_dict)

    return jsonify(all_tobs)


# ************* Date *********************

@app.route("/api/v1.0/<stdate>")
def startDateOnly(stdate):
    
    print(f"Incoming parameter: {stdate}")

    session = Session(engine)


    sel_values = [
                  func.max(Measurement.tobs), 
                  func.min(Measurement.tobs),
                  func.avg(Measurement.tobs)]
   

    results = session.query(*sel_values).filter(Measurement.date >= stdate).all()


    session.close()

    # Create a dictionary from the row data and append to a list of all_stations
    all_stats = []
    for maxval,minval, avgval in results:
      
        
        xx_dict = {}        
        xx_dict["Min Temp"] = minval
        xx_dict["Max Temp"] = maxval
        xx_dict["Avg Temp"] = avgval

        print(xx_dict)
        all_stats.append(xx_dict)


    return jsonify(xx_dict)


# ************* Start Date and End Date *********************

@app.route("/api/v1.0/<stdate>/<enddate>")
def DateBetween(stdate,enddate):
    
    print(f"Incoming parameter: {stdate}")
    print(f"Incoming parameter: {enddate}")

    session = Session(engine)


    sel_values = [
                  func.max(Measurement.tobs), 
                  func.min(Measurement.tobs),
                  func.avg(Measurement.tobs)]
   

    results = session.query(*sel_values).filter(Measurement.date >= stdate).\
                                         filter(Measurement.date <= enddate).all()


    session.close()

    # Create a dictionary from the row data and append to a list of all_stations
    all_stats = []
    for maxval,minval, avgval in results:
      
        
        xx_dict = {}        
        xx_dict["Min Temp"] = minval
        xx_dict["Max Temp"] = maxval
        xx_dict["Avg Temp"] = avgval

        print(xx_dict)
        all_stats.append(xx_dict)


    return jsonify(xx_dict)


if __name__ == '__main__':
    app.run(debug=True)
