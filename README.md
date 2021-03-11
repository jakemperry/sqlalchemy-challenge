# sqlalchemy-challenge

This project contains a jupyter notebook to set up sqlalchemy queries with a sqlite database of weather data from Hawaii.  These queries are the basis for a Flask app which can be used to generate queries from the sqlite database and display them in your browser.

## Routes

The Flask app has the following routes:

|Route|Description|
|---|---|
|/api/v1.0/precipitation|Returns a JSON object with dates and the sum of precpitation for the last year of data in the sqlite database.|
|/api/v1.0/stations|Returns a JSON object with weather station IDs and the count of temperature observations from these stations in the database.|
|/api/v1.0/tobs|Returns a JSON object with all of the temperature observations from the most active weather station for the last year of data in the database.|
|/api/v1.0/&lt;start&gt;|Returns a JSON object with the min, max, and avg temperature for all weather stations, starting with the date specified and proceeding thorugh all dates after the start date.  **Must specify date in 'YYYY-MM-DD' format.**
|/api/v1.0/&lt;start&gt;/&lt;end&gt;|Returns a JSON object with the min, max, and avg temperature for all weather stations, starting with the start date specified thorugh the end date specified.  **Must specify dates in 'YYYY-MM-DD' format.**

## Required Python Modules
- sqlalchemy
- pandas
- datetime
- flask
- numpy
- matplotlib