import json
import httplib2 as http 
from urllib.parse import urlparse

import pandas as pd

# API Call Settings
uri = "http://datamall2.mytransport.sg/"
with open("../../python_repo_doc/bus_arrival_doc/LTA_AccountKey") as k: # type: ignore
    key = k.readlines()

method = "GET"
body = ""
h = http.Http()
headers = {"AccountKey": key[0],
           "accept": "application/json"}

# Define function to retrieve all available bus stops in Singapore
def retrieve_bus_stops():
    
    # Create list of containers
    busStopCode = list()
    roadName = list()
    description = list()
    latitude = list()
    longitude = list()

    # Each API call only returns 500 records.
    # Total number of bus stops in Singapore slightly > 5,000
    for i in range(0, 5500, 500):
        
        # Iterating through each call of 500 records.
        target = urlparse(uri + "ltaodataservice/BusStops?$skip=" + str(i))
        
        response, content = h.request(
            target.geturl(),
            method,
            body,
            headers
            )
        
        jsonObj = json.loads(content)
        
        busStopCode.extend([i["BusStopCode"] for i in jsonObj["value"]])
        roadName.extend([i["RoadName"] for i in jsonObj["value"]])
        description.extend([i["Description"] for i in jsonObj["value"]])
        latitude.extend([i["Latitude"] for i in jsonObj["value"]])
        longitude.extend([i["Longitude"] for i in jsonObj["value"]])

    # Build all the responses into a dataframe for output
    bs_df = pd.DataFrame({"busStopCode": busStopCode,
                        "roadName": roadName,
                        "description": description,
                        "latitude": latitude,
                        "longitude": longitude})
    
    return bs_df

