# IMPORT OF LIBRARIES ---------
# FLASK APP BY ERICK HERNANDEZ

from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import Column, Integer, String, Float

# DEFINE SESSION AND ENGINE ---------

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

measures = Base.classes.measurement
stations = Base.classes.station

session = Session(engine)

# IDENTIFY CLASSES -----------

class MEAS(measures):
    __tablename__ = "measures_table"
    id = Column(Integer, primary_key=True)
    station = Column(String)
    date = Column(String)
    prcp = Column(Float)
    tobs = Column(Integer)
    
class STAT(stations):
    __tablename__ = "stations_table"
    id = Column(Integer, primary_key=True)
    station = Column(String)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    elevation = Column(Float)

# ------------- FLASK APPLICATION -----------

app = Flask(__name__)

# HOME FUNCTION ----------

@app.route("/")
def home():
    return f"""
    <h1>Welcome to Hawaii Climate API!</h1>
    <p>By Erick Hernandez</p>
    <p>---------------------------------</p>
    <h3>Routes available:</h3>
    <p>/api/v1.0/precipitation (for total data registered)</p>
    <p>/api/v1.0/stations (for stations that gathered the information)</p>
    <p>/api/v1.0/tobs (for the station USC00519281, starting 2016-08-23)</p>
    <p>/api/v1.0/start-date as (YYYY-MM-DD)</p>
    <p>/api/v1.0/start-date/end-date as (YYYY-MMM-DD)</p>
    <p>-----------------------------</p>"""

# PRECIPITATION FUNCTION -------------

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(measures.date, measures.prcp).all()
    session.close()
    
    rainy = []

    for date, rain in results:
        rainy.append({
            "date": date,
            "rain": rain
        })

    return jsonify(rainy)

# STATIONS FUNCTION ------------------

@app.route("/api/v1.0/stations")
def my_stations():
    print("Available stations:")
    session = Session(engine)
    results = session.query(stations.name).all()
    session.close()
    return jsonify(results)

# TOBS FUNCTION ---------------------

@app.route("/api/v1.0/tobs")
def tobs1():
    print(f"TOBS for station USC00519281, from 2016-08-23 to 2017-08-23")
    session = Session(engine)
    results = session.query(measures.tobs).filter(measures.station == "USC00519281", measures.date >= "2016-08-23")
    session.close()

    my_results = []

    for x in results:
        my_results.append(x)
    return jsonify(my_results) 

# START DATE FUNCTION ---------------

@app.route("/api/v1.0/<start>")
def start_date(start):
    print(f"Start date given {start}")
    clean_date = start.replace("/","-")

    list1 =[]

    session = Session(engine)
    results = session.query(measures.tobs).filter(measures.date >= clean_date).all()
    session.close()

    for x in results:
        list1.append(x[0])

    list1 = [round(x) for x in list1]
    my_min = min(list1)
    my_max = max(list1)
    my_avg = round(sum(list1)/len(list1),0)
    return f'''
    <p>-------------------------------------------</p>
    <p>TOBS data from: {clean_date} to 2017-08-23</p>
    <p>Min TOBs is {my_min}</p>
    <p>Max TOBs is {my_max}</p>
    <p>Average TOBs is {my_avg}</p>
    <p>--------------------------------------------</p>'''

# START AND END DATE FUNCTION --------------------

@app.route("/api/v1.0/<start>/<end>")
def defined_dates(start, end):
    print(f"Start date given {start}, end date given {end}")
    clean_start = start.replace("/","-")
    clean_end = end.replace("/","-")

    list2 =[]

    session = Session(engine)
    results = session.query(measures.tobs).filter(measures.date >= clean_start, measures.date <= clean_end).all()
    session.close()

    for x in results:
        list2.append(x[0])

    list2 = [round(x) for x in list2]
    my_min = min(list2)
    my_max = max(list2)
    my_avg = round(sum(list2)/len(list2),0)
    return f'''
    <p>-------------------------------------------</p>
    <p>TOBS data from: {clean_start} to {clean_end}</p>
    <p>Min TOBs is {my_min}</p>
    <p>Max TOBs is {my_max}</p>
    <p>Average TOBs is {my_avg}</p>
    <p>--------------------------------------------</p>'''


# DEBUG FUNCTION ------------

if __name__ == "__main__":
    app.run(debug=True)