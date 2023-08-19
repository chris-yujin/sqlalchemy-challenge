# Import the dependencies.
from pathlib import Path 
import sqlalchemy
from sqlalchemy import create_engine, text, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session 
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
#database_path = Path("Resources/hawaii.sqlite")
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################




#################################################
# Flask Routes
#################################################
