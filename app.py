# Import the dependencies.
from pathlib import Path 
import sqlalchemy
from sqlalchemy import create_engine, text, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session 
from flask import Flask, jsonify
import numpy as np
import datetime as dt


#################################################
# Database Setup
#################################################
#database_path = Path("Resources/hawaii.sqlite")
# database_path = Path()
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

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
    return (
        f"Welcome to the Surfer Weather API!</br>"
        f"Explore the weather for surfing</br>"
        
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation</br>"
        f"/api/v1.0/stations</br>"
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/<start></br>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    latest_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    latest_date = latest_date[0]
    latest_date
    # Convert the string '2017-08-23' to a datetime object
    latest_date_datetime = dt.datetime.strptime(latest_date, '%Y-%m-%d')

    # Calculate one year before the latest date

    delta_date = latest_date_datetime-dt.timedelta(days=365)
    delta_date = delta_date.strftime('%Y-%m-%d')
    delta_date
    precipitation_year = session.query(measurement.date, measurement.prcp).filter(measurement.date <= latest_date, measurement.date >= delta_date)
    session.close()
    all_precipitation = []
    for date, prcp in precipitation_year:
        results_dict = {}
        results_dict["date"] = date
        results_dict["prcp"] = prcp
        all_precipitation.append(results_dict)
    return jsonify(all_precipitation)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    all_stations_query = session.query(station.station, station.name, station.latitude, station.longitude, station.elevation).all()
    session.close()
    all_stations = []
    for station_id, name, latitude, longitude, elevation in all_stations_query:
        station_dictionary = {}
        station_dictionary['station_id'] = station_id
        station_dictionary['name'] = name
        station_dictionary['latitude'] = latitude
        station_dictionary['longitude'] = longitude
        station_dictionary['elevation'] = elevation
        all_stations.append(station_dictionary)
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    most_active_stations = session.query(measurement.station, func.count(measurement.station)).group_by(measurement.station).order_by(func.count(measurement.station).desc()).all()
    single_most_active_station = most_active_stations[0][0]
    latest_date_most_active_station = session.query(measurement.date).order_by(measurement.date.desc()).filter(measurement.station == single_most_active_station).first()
    latest_date_most_active_station = latest_date_most_active_station[0]

    # Convert the string '2017-08-18' to a datetime object
    latest_date_datetime = dt.datetime.strptime(latest_date_most_active_station, '%Y-%m-%d')

    # Calculate one year before the latest date

    one_year = latest_date_datetime-dt.timedelta(days=365)
    one_year = one_year.strftime('%Y-%m-%d')
    one_year


    most_active_station_query = session.query(measurement.tobs).filter(measurement.date <= latest_date_most_active_station, measurement.date >= one_year).filter(measurement.station == single_most_active_station).all()
    session.close()
    most_active = list(np.ravel(most_active_station_query))
    return jsonify(most_active)

@app.route("/api/v1.0/<start>")
def start_temp(start):
    session = Session(engine)
    results = session.query(func.min(measurement.tobs), 
                            func.max(measurement.tobs), 
                            func.avg(measurement.tobs)).filter(measurement.date >= start).all()
    session.close()
    results_dictionary = {}
    results_dictionary["min_temp"] = results[0][0]
    results_dictionary["max_temp"] = results[0][1]
    results_dictionary["avg_temp"] = results[0][2]
    return jsonify(results_dictionary)

@app.route("/api/v1.0/<start>/<end>")
def start_end_temp(start, end):
    session = Session(engine)
    results = session.query(func.min(measurement.tobs), 
                            func.max(measurement.tobs), 
                            func.avg(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end).all()
    session.close()
    results_dictionary = {}
    results_dictionary["min_temp"] = results[0][0]
    results_dictionary["max_temp"] = results[0][1]
    results_dictionary["avg_temp"] = results[0][2]
    return jsonify(results_dictionary)


if __name__ == "__main__":
    app.run(debug=True)