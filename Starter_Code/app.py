from flask import Flask, jsonify


import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


app= Flask(__name__)

#connect to the database
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base= automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement=Base.classes.measurement
Station=Base.classes.station

# Create our session (link) from Python to the DB
session=Session(engine)


#home route
@app.route("/")
def home():
    return (
          f"<center><h2>welcome to the Hawaii climate analysis local API!</h2<>/centre>"
          f"<center><h3>select frrom one of the available routes:</h3<>/centre>"
          f"<center>/api/v1.0/precipitation</centre>"
          f"<center>/api/v1.0/stations</centre>"
          f"<center>/api/v1.0/tobs</centre>"
          f"<center>/api/v1.0/start/end</centre>"
          )


#/api/v1.0/precipitation route
@app.route("/api/v1.0/precipitation")
def precip():
    # return the previous year's precipitation as a json
    # Calculate the date one year from the last date in data set.
    previousYear = dt.date(2017,8,23)- dt.timedelta(days=365)
    #previousYear

    # Perform a query to retrieve the data and precipitation scores
    results=session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >=previousYear).all()

    session.close()
    #dictionary with the date as the key and the precipitation (prcp) as the value
    precipitation = {date: prcp for date, prcp in results}
    #convert to a json
    return jsonify(precipitation)
#

#/api/v1.0/station route
@app.route("/api/v1.0/stations")
def stations():
    # show a list of stations
    #perform a query to retrieve the names of the stations
    results = session.query (Station.station) .all()
    session.close
    
    stationList = list(np.ravel(results))


    #convert to a json and display
    return jsonify(stationList)



#/api/v1.0/tobs route
@app.route("/api/v1.0/tobs")
def temperature():
    # return the previous year's temperature
    # Calculate the date one year from the last date in data set.
    previousYear = dt.date(2017,8,23)- dt.timedelta(days=365)
    #previousYear

    # Perform a query to retrieve the temperature from the most active station from the past year
    results= session.query(Measurement.tobs).\
             filter(Measurement.station== 'USC00519281').\
             filter(Measurement.date>= previousYear).all()
    
    session.close()

       
    temperatureList= list(np.ravel(results))

    #return the list of temperature
    return jsonify(temperatureList)


#/api/v1.0/start/end and /api/v1.0/start route
@app.route("/api/v1.0/<start?")
@app.route("/api/v1.0/<start>/<end>")
def datestats (start=None, end = None):
     
     #select statements
     selection = [func.min(Measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)]

     if not end:
          
          startdate = dt.datetime.strptime(start, "%m%d%y")

          results = session.query(*selection).filter(measurement.date>=startdate)

          session.close()


          temperatureList= list(np.ravel(results))

             #return the list of temperature
          return jsonify(temperatureList)


     else:
          
            startdate = dt.datetime.strptime(start, "%m%d%y")
            endDate= dt.datetime.strptime(end, "%m%d%y")

            results = session.query(*selection)\
                    .filter(Measurement.date>=startdate)\
                    .filter(Measurement.date>=endDate).all()
            

            session.close()


            temperatureList= list(np.ravel(results))

             #return the list of temperature
            return jsonify(temperatureList)

 

           ## app launcher
if __name__ == '__main__': 
        app.run(debug=True)