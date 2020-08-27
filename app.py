#Now that you have completed your initial analysis, design a Flask API based on the queries that you have just developed.
#start-start/end
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

#dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify
import numpy as np

#database setup
#create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#reflect esisting database into new model
Base = automap_base()

#reflect the tables
Base.prepare(engine, reflect=True)

#save references to the tables
Base.classes.keys()
Measurement = Base.classes.measurement
Station = Base.classes.station

#Flask setup
app = Flask(__name__)


#Routes - home - list all routes
@app.route("/")
def welcome():
    return(
    f"Wecome to the Hawaii climate analysis home page!<br/>"
    f"<br/>"
    f"Available Routes:<br/>"
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/date - (enter date format as: yyyy-mm-dd)<br/>"
    f"/api/v1.0/start/end - (enter date format as: yyyy-mm-dd)")

#Convert the query results to a dictionary using date as the key and prcp as the value. Return JSON representation of the dictionary.
#Routes - Precip
@app.route("/api/v1.0/precipitation")
def precipitation():
    #create session
    session = Session(engine)
    #query to find precip and date - does not specify to limit to one year so querying all data
    results = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date).all()
    session.close()
    #create list in dict format - date as key and prcp as value
    precip = []
    for date, prcp in results:
        pdict = {date:prcp}
        precip.append(pdict)
    #print list as JSON
    return jsonify(precip)
 
    
#Return a JSON list of stations from the dataset
#Routes - Stations
@app.route("/api/v1.0/stations")
def stations():
    #create session
    session = Session(engine)
    # query to return all stations
    results = session.query(Station.station).all()
    session.close()
    #convert to list
    stations = list(np.ravel(results))
    #print list as JSON
    return jsonify(stations)


#Query the dates and temperature observations of the most active station for the last year of data. Return a JSON list.
#last date was found in previous .ipynb query - 2017-8-23
#most active station was found in previous .ipynb query - 'USC00519281'
#Routes - Temps
@app.route("/api/v1.0/tobs")
def tobs():
    #create session
    session = Session(engine)
    #Calculate new data 1 year ago from last date
    oneyear = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # query to return date and temps for one year for most active station
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= oneyear).filter(Measurement.station == 'USC00519281').order_by(Measurement.date).all()
    session.close()
    #convert to normal list 
    temps = list(np.ravel(results))
    #OR for a nicer dictionary list output - hw prompt only asks for JSON list
    #comment out the line above and uncomment the below to run
    #create list in dict format
#     temps = []
#     for date, tobs in results:
#         tdict = {}
#         tdict['date']=date
#         tdict['temp']=tobs
#         temps.append(tdict)
    #print list as JSON
    return jsonify(temps)


#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start date
#Routes - start
@app.route("/api/v1.0/<start>")
def start(start=None):
    #create session
    session = Session(engine)
    #query to find the temp min, avg, and max at a given start date
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).all()
    session.close()
    #convert to list
#     stattemps = list(np.ravel(results))    
    #OR for more complex list format - labels!
    #create list in dict format
    stattemps = []
    for result in results:
        statdict = {}
        statdict['Date'] = start
        statdict['Average Temperature'] = result[1]
        statdict['Highest Temperature'] = result[2]
        statdict['Lowest Temperature'] = result[3]
        stattemps.append(statdict)
    #print results as JSON
    return jsonify(stattemps)
    
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start-end range    
#Routes - start/end
@app.route("/api/v1.0/<start>/<end>")
def start_end(start=None, end=None):
    #create session
    session = Session(engine)
    #query to find the temp min, avg, and max at a given start-end range
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).all()    
    session.close()
    #convert to list
#     stattemps2 = list(np.ravel(results))    
    #OR for more complex list format - labels!
    #create list in dict format
    stattemps2 = []
    for result in results:
        statdict2 = {}
        statdict2['Date'] = start
        statdict2['End Date'] = end
        statdict2['Average Temperature'] = result[1]
        statdict2['Highest Temperature'] = result[2]
        statdict2['Lowest Temperature'] = result[3]
        stattemps2.append(statdict2)
    #print results as JSON
    return jsonify(stattemps2)
    
#end code to run all
if __name__ == '__main__':
    app.run(debug=True)