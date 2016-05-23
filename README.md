# GrafanaSQL
A InfluxDB mimic layer.

## How it works?
GrafanaSQL is written in python 2.7 using Flask and others libs.
He catch the requests, do it in SQL and reply with a json like InfluxDB.

## Setup and Play
Download the master, install the dependecies 
 * flask
 * flask_sqlalchemy
 
Run GrafanaSQL `python2.7 GrafanaSQL.py`

In your Grafana data source add *InfluxDB 0.9.X*.
GrafanaSQL server run on port 4000 (configurable for the next release)

In a new dashboard switch editor mode and paste the following query: <br>
`select timestamp as time,value from measurements where measure == 'ot' AND timerange($timeFilter,'%Y-%m-%d %H:%M:%S')`

Enjoy ...

# Mandatory
* Timestamp as a first field and renamed time
* timerange($timeFilter, 'Timestamp format')
