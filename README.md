# sqlalchemy-challenge

Resources Folder:
	This folder holds the sqlite used in the Jupyter Notebook and Python scripts. It also has the CSV files for 
measurements and stations.

app.py:
	This file creates an API for viewing the data base. The dates used in the start and start/end routes should be
entered in the YYYY-MM-DD format.

climate_starter.ipynb:
	This Jupyter Notebook uses SQLAlchemy to retrieve the last 12 months of precipitation data and save it to a
data frame as well as visualize the data. It also retrieves data for the stations, finds the most active station and 
saves the data in a data fram for visualization.
